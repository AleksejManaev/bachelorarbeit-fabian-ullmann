import re

from django.db.models import Q
from django.http import HttpResponseForbidden

from mentoring.models import AbstractWork, Comment


class AccessControlMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        request_url = request.path

        if re.fullmatch('/(student|tutor|comments)/.*', request_url):
            if not hasattr(request.user, 'portaluser'):
                return HttpResponseForbidden()

            if request_url.startswith('/student'):
                # Der Student darf auf student-Views zugreifen, der Tutor nicht
                if hasattr(request.user.portaluser, 'student'):
                    return None
                elif hasattr(request.user.portaluser, 'tutor'):
                    return HttpResponseForbidden()
            elif request_url.startswith('/tutor'):
                # Der Student darf nicht auf tutor-Views zugreifen, der Tutor darf auf tutor-Views zugreifen, aber für einige Views wird eine zusätzliche Berechtigung verlangt
                if hasattr(request.user.portaluser, 'student'):
                    return HttpResponseForbidden()
                elif hasattr(request.user.portaluser, 'tutor'):
                    if request_url.startswith('/tutor/placementseminar'):
                        if request.user.portaluser.tutor.placement_responsible:
                            return None
                        else:
                            return HttpResponseForbidden()
                    elif re.fullmatch('/tutor/thesis.*seminar.*', request_url):
                        if request.user.portaluser.tutor.thesis_responsible:
                            return None
                        else:
                            return HttpResponseForbidden()
                    elif request_url.startswith('/tutor/posters'):
                        if request.user.portaluser.tutor.poster_responsible:
                            return None
                        else:
                            return HttpResponseForbidden()
                    elif re.fullmatch('/tutor/(placement|thesis)/.*', request_url):
                        # Der Tutor darf nur auf Praktika oder Abschlussarbeiten zugreifen, die ihm vom Studenten zur Betreuung freigegeben wurden
                        if AbstractWork.objects.filter(id=view_kwargs['pk'], tutor=request.user.portaluser.tutor, mentoring_requested=True).exists():
                            return None
                        else:
                            return HttpResponseForbidden()
                    else:
                        return None
            elif re.fullmatch('/comments/abstractwork/\d+', request_url):
                # Nur der beteiligte Student und Tutor dürfen Kommentare zum Praktikum oder Abschlussarbeit einsehen und erstellen
                if AbstractWork.objects.filter(Q(id=view_kwargs['pk']), Q(student=request.user.portaluser) | Q(tutor=request.user.portaluser)).exists():
                    return None
                else:
                    return HttpResponseForbidden()
            elif re.match('/comments/abstractwork/toggleprivacy', request_url):
                # Nur der Ersteller des Kommentars darf die Sichtbarkeit des Kommentars ändern
                if Comment.objects.filter(id=request.POST.get('id'), author=request.user.id).exists():
                    return None
                else:
                    return HttpResponseForbidden()
        else:
            return None
