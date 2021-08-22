from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Review
from .forms import ReviewForm


def reviews(request):
    """
    A view showing all reviews
    """
    reviews = Review.objects.all()

    context = {
        'reviews': reviews,
    }

    return render(request, 'reviews/reviews.html', context)


@login_required
def add_review(request):
    """
    A view for logged in users to add a review
    """
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks! Your review was added')
            
            return redirect(reverse('reviews',))
        else:
            messages.error(request, 'Failed to add review.\
                                    Please ensure form is valid and try again.')
    else:
        form = ReviewForm()

    form = ReviewForm()
    template = 'reviews/add_review.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_review(request, review_id):
    """
    A view for logged in users to edit their review
    """
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review was successfully edited.')

            return redirect(reverse('reviews'))
        else:
            messages.error(request, 'Failed to edit review. \
                    Please check the form is valid and try again.')
    else:
        form = ReviewForm(instance=review)

    template = "reviews/edit_review.html"
    context = {
        "form": form,
        "review": review,
    }

    return render(request, template, context)


@login_required
def delete_review(request, review_id):
    """
    A view for logged in users to delete their review
    """
    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    messages.success(request, 'Your review was deleted!')

    return redirect(reverse('reviews'))
