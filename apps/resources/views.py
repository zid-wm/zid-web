import boto3

from django.shortcuts import render, redirect

from apps.administration.models import ActionLog
from apps.resources.forms import AddFileForm
from zid_web.decorators import require_staff, require_member


@require_member
def view_files(request):
    s3_client = boto3.client('s3')
    s3_objects = s3_client.list_objects_v2(Bucket='zid-files')

    files = []
    for f in s3_objects['Contents']:
        data = f['Key'].split('/')
        files.append({
            'category': data[0],
            'name': data[1],
            'key': f['Key'],
            'updated': f['LastModified']
        })

    # TODO: This can definitely stand to be refactored somehow
    vrc_files = [f for f in files if f['category'] == 'vrc' and len(f['name']) > 0]
    vstars_files = [f for f in files if f['category'] == 'vstars' and len(f['name']) > 0]
    veram_files = [f for f in files if f['category'] == 'veram' and len(f['name']) > 0]
    vatis_files = [f for f in files if f['category'] == 'vatis' and len(f['name']) > 0]
    sop_files = [f for f in files if f['category'] == 'sop' and len(f['name']) > 0]
    loa_files = [f for f in files if f['category'] == 'loa' and len(f['name']) > 0]
    mavp_files = [f for f in files if f['category'] == 'mavp' and len(f['name']) > 0]
    misc_files = [f for f in files if f['category'] == 'misc' and len(f['name']) > 0]

    return render(request, 'files.html', {
        'page_title': 'Files',
        'vrc_files': vrc_files,
        'vstars_files': vstars_files,
        'veram_files': veram_files,
        'vatis_files': vatis_files,
        'sop_files': sop_files,
        'loa_files': loa_files,
        'mavp_files': mavp_files,
        'misc_files': misc_files
    })


@require_staff
def add_file(request):
    if request.method == 'POST':
        s3 = boto3.client('s3')
        # TODO: Make sure file with this name doesn't exist
        s3.upload_fileobj(
            request.FILES['file'],
            'zid-files',
            f'{request.POST["category"]}/{request.POST["file_name"]}',
            ExtraArgs={
                'ACL': 'public-read'
            }
        )

        ActionLog(
            action=f'{request.user_obj.full_name} uploaded a file: {request.POST["file_name"]}'
        ).save()

        return redirect('/files')
    else:
        form = AddFileForm()
        return render(request, 'add_file.html', {
            'page_title': 'Add File',
            'form': form
        })


@require_staff
def delete_file(request, file_cat, file_name):
    s3 = boto3.client('s3')
    s3.delete_object(
        Bucket='zid-files',
        Key=f'{file_cat}/{file_name}'
    )

    ActionLog(
        action=f'{request.user_obj.full_name} deleted a file: {file_name}'
    ).save()

    return redirect('/files')

