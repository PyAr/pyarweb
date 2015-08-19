from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import ProfileForm, ProfilesMediosContactosFormSet
from .models import Profiles

@login_required
def update_profile(request):
    """
    Create or update user profile
    """
    user_id = request.user.id

    try:
        perfil = Profiles.objects.get(user=user_id)
    except Profiles.DoesNotExist:
        perfil = None

    form_perfil = ProfileForm(instance=perfil)
    form_medios_ctos = ProfilesMediosContactosFormSet(instance=perfil)

    ctx = {
        'form_perfil': form_perfil,
        'form_medio_ctos': form_medios_ctos
    }

    if request.method == 'POST':
        form_perfil = ProfileForm(request.POST, instance=perfil)
        if form_perfil.is_valid():
            perfil_instance = form_perfil.save(commit=False)
            form_medios_ctos = ProfilesMediosContactosFormSet(request.POST, instance=perfil_instance)

            if form_medios_ctos.is_valid():
                # -- save perfil
                perfil_instance.user_id = user_id
                perfil_instance.save()
                # -- to save tags
                form_perfil.save_m2m()
                # -- save medios contactos
                form_medios_ctos.save()
            else:
                ctx = {'form_medio_ctos': form_medios_ctos}

            messages.success(request, 'Perfil Actualizado')
            return HttpResponseRedirect(reverse("homepage"))
        else:
            ctx = {'form_perfil': form_perfil}

    return render(request, 'profiles/profile_form.html', ctx)
