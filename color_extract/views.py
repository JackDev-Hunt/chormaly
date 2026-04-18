from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .utils import extract_colors_from_html, extract_colors_from_css

def home(request):
    """হোম পেজ - ফাইল আপলোড ফর্ম"""
    return render(request, 'color_extract/home.html')

@csrf_exempt
def extract_colors(request):
    """HTML বা CSS ফাইল আপলোড করে কালার এক্সট্রাক্ট করা"""
    
    # Check if this is a POST request with file
    if request.method == 'POST':
        
        # Check if ad_shown parameter is present
        ad_shown = request.POST.get('ad_shown', 'false')
        
        # If this is the first request (ad not shown yet)
        if ad_shown == 'false' and request.FILES.get('file'):
            uploaded_file = request.FILES['file']
            filename = uploaded_file.name
            
            # ফাইল সাইজ চেক (10MB limit)
            if uploaded_file.size > 10 * 1024 * 1024:
                messages.error(request, 'File too large! Maximum size is 10MB.')
                return redirect('home')
            
            # Store file info in session temporarily
            request.session['pending_file'] = {
                'name': filename,
                'content': uploaded_file.read().decode('utf-8', errors='ignore'),
                'size': uploaded_file.size
            }
            request.session.modified = True
            
            return render(request, 'color_extract/ad_page.html', {
                'filename': filename,
                'file_size': uploaded_file.size
            })
        
        # If ad already shown, process the file from session
        elif ad_shown == 'true':
            pending_file = request.session.get('pending_file')
            
            if not pending_file:
                messages.error(request, 'Session expired. Please upload file again.')
                return redirect('home')
            
            filename = pending_file['name']
            file_content = pending_file['content']
            
            # ফাইল টাইপ চেক
            is_html = filename.lower().endswith(('.html', '.htm'))
            is_css = filename.lower().endswith('.css')
            
            if not (is_html or is_css):
                messages.error(request, 'Only .html, .htm or .css files allowed!')
                # Clear session on error
                if 'pending_file' in request.session:
                    del request.session['pending_file']
                    request.session.modified = True
                return redirect('home')
            
            try:
                # ফাইল টাইপ অনুযায়ী এক্সট্রাক্ট
                if is_html:
                    colors_dict = extract_colors_from_html(file_content)
                    file_type = 'HTML'
                else:
                    colors_dict = extract_colors_from_css(file_content)
                    file_type = 'CSS'
                
                # Clear session after successful processing
                if 'pending_file' in request.session:
                    del request.session['pending_file']
                    request.session.modified = True
                
                # Check if colors_dict is a dictionary (from your utils)
                if isinstance(colors_dict, dict):
                    # Your utils returns dictionary format
                    return render(request, 'color_extract/result.html', {
                        'colors': colors_dict,
                        'filename': filename,
                        'file_type': file_type,
                        'total_count': colors_dict.get('total_count', 0)
                    })
                else:
                    # If it returns list format (fallback)
                    all_colors = list(set(colors_dict)) if colors_dict else []
                    return render(request, 'color_extract/result.html', {
                        'colors': all_colors,
                        'filename': filename,
                        'file_type': file_type,
                        'total_count': len(all_colors)
                    })
                
            except Exception as e:
                messages.error(request, f'Error extracting colors: {str(e)}')
                # Clear session on error
                if 'pending_file' in request.session:
                    del request.session['pending_file']
                    request.session.modified = True
                return redirect('home')
    
    return redirect('home')

def about(request):
    """অ্যাপ সম্পর্কে তথ্য পেজ"""
    return render(request, 'color_extract/about.html')

def track_ad_click(request):
    """Track ad clicks for analytics"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Ad clicked at: {data.get('timestamp')}")
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'error'}, status=400)
    return JsonResponse({'status': 'method not allowed'}, status=405)