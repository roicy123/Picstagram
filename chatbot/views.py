# chatbot/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from .services.groq_service import GroqService
from .services.image_service import ImageGenerationService
import json

@login_required
def chat_view(request):
    conversations = Conversation.objects.filter(user=request.user).order_by('-updated_at')
    
    # Get active conversation or create new one
    conversation_id = request.GET.get('conversation_id')
    if conversation_id:
        active_conversation = Conversation.objects.get(id=conversation_id, user=request.user)
    else:
        active_conversation = Conversation.objects.create(user=request.user)
    
    context = {
        'conversations': conversations,
        'active_conversation': active_conversation,
    }
    
    return render(request, 'chatbot/chat.html', context)

@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        conversation_id = data.get('conversation_id')
        message_text = data.get('message')
        
        # Get or create conversation
        if conversation_id:
            conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        else:
            conversation = Conversation.objects.create(user=request.user)
        
        # Save user message
        Message.objects.create(
            conversation=conversation,
            role='user',
            content=message_text
        )
        
        # Check if this is an image generation request
        if message_text.lower().startswith("generate image:") or message_text.lower().startswith("create image:"):
            image_prompt = message_text.split(":", 1)[1].strip()
            image_service = ImageGenerationService()
            result = image_service.generate_image(image_prompt)
            
            if result['status'] == 'success':
                # Save assistant message with image
                assistant_message = Message.objects.create(
                    conversation=conversation,
                    role='assistant',
                    content=f"Here's the image I created based on: {image_prompt}",
                    image_url=result['image']
                )
                
                return JsonResponse({
                    'status': 'success',
                    'message': assistant_message.content,
                    'image': result['image'],
                    'timestamp': assistant_message.created_at.isoformat()
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': result['message']
                })
        
        # For regular text chat
        else:
            # Get conversation history
            message_history = list(conversation.messages.values('role', 'content'))
            
            # Get response from Groq
            groq_service = GroqService()
            response = groq_service.get_response(message_history)
            
            if response['status'] == 'success':
                # Save assistant response
                assistant_message = Message.objects.create(
                    conversation=conversation,
                    role='assistant',
                    content=response['message']
                )
                
                # Update conversation title if this is the first exchange
                if conversation.messages.count() <= 3 and conversation.title == "New Conversation":
                    # Create a title based on the first user message
                    first_msg = conversation.messages.filter(role='user').first()
                    if first_msg:
                        title = first_msg.content[:50] + "..." if len(first_msg.content) > 50 else first_msg.content
                        conversation.title = title
                        conversation.save()
                
                return JsonResponse({
                    'status': 'success',
                    'message': assistant_message.content,
                    'conversation_id': conversation.id,
                    'conversation_title': conversation.title,
                    'timestamp': assistant_message.created_at.isoformat()
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': response['message']
                })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
