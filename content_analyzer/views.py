# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .services import ContentAnalyzerService
from .models import ContentAnalysis

@login_required
def analyze_content(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        post_type = request.POST.get('post_type', 'general')
        
        analyzer = ContentAnalyzerService()
        analysis = analyzer.analyze_content(request.user, content, post_type)
        
        if analysis:
            return JsonResponse({
                'success': True,
                'analysis_id': analysis.id,
                'is_safe': analysis.is_safe,
                'sentiment': analysis.sentiment,
                'engagement_score': analysis.engagement_score,
                'improved_content': analysis.improved_content
            })
        
        return JsonResponse({'success': False, 'error': 'Analysis failed'})
    
    return render(request, 'analyzer/analyze.html')

@login_required
def analysis_history(request):
    analyses = ContentAnalysis.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'analyzer/history.html', {'analyses': analyses})
