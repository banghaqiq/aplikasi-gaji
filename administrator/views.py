from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,Group
from .models import Guru, Detail_gaji, Piket, Tahun_pelajaran, Jam_pelajaran, Setting_gaji
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .decorators import ijinkan_pengguna, pilihan_login, tolakhalaman_ini
from .forms import TahunForm, JamForm, SettingForm,PiketForm,GuruForm,UserForm,DetailForm
from django.db.models.functions import ExtractMonth
from django.contrib import messages

import calendar

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

@tolakhalaman_ini
def halamanlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'Username Tidak ditemukan')
            return redirect('halamanlogin')
        cocokan = authenticate(request, username=username, password=password)
        if cocokan is None:
            messages.success(request, 'Password salah')
            return redirect('halamanlogin')
        if cocokan is not None:
            login(request, cocokan)
            return redirect('berandaadmin')
    context = {
        'judul': 'Halaman Login',
    }
    return render(request, 'halamanlogin.html', context)
def logoutPage(request):
    logout(request)
    return redirect('halamanlogin')

@login_required(login_url='halamanlogin')
@pilihan_login
def berandaadmin(request):
    jmlGuru = Guru.objects.all().count()
    jmlPiket = Piket.objects.all().count()
    jmlTahun = Tahun_pelajaran.objects.all().count()
    jmlJam = Jam_pelajaran.objects.all().count()
    context = {
        'judul': 'Halaman Beranda',
        'menu': 'Beranda',
        'jmlGuru':jmlGuru,
        'jmlPiket':jmlPiket,
        'jmlTahun':jmlTahun,
        'jmlJam':jmlJam
        
        
        
 
     
    }
    return render(request, 'beranda_admin.html', context)


@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def tahunpelajaran(request):
    tahun = Tahun_pelajaran.objects.all().order_by('-id')
    context = {
        'judul': 'Halaman Tahun Pelajaran',
        'menu': 'Tahun Pelajaran',
        'data':tahun,
    }
    return render(request, 'tahunpelajaran_admin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def formtahunadmin(request):
    form = TahunForm()
    if request.method == 'POST':
        formsimpan = TahunForm(request.POST)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('tahunpelajaran')
    context = {
        'judul': 'Form Tahun Pelajaran',
        'menu': 'Tahun Pelajaran',
        'form':form
    }
    return render(request, 'formtahunadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def edittahunadmin(request, pk):
    tahun = Tahun_pelajaran.objects.get(id=pk)
    form = TahunForm(instance=tahun)
    if request.method == 'POST':
        formsimpan = TahunForm(request.POST, instance=tahun)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('tahunpelajaran')
    context = {
        'judul': 'Formedit Tahun Pelajaran',
        'menu': 'Tahun Pelajaran',
        'form':form
    }
    return render(request, 'formtahunadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def deletetahunadmin(request, pk):
    hapus = Tahun_pelajaran.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('tahunpelajaran')

    context = {
        'judul': 'Hapus Tahun Pelajaran',
        'menu': 'Tahun Pelajaran',
        'hapus':hapus  
    }
    return render(request, 'hapustahunadmin.html', context)


@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def jampelajaran(request):
    jam = Jam_pelajaran.objects.all().order_by('jam_ke')
    context = {
        'judul': 'Halaman Jam Pelajaran',
        'menu': 'Jam Pelajaran',
        'data':jam,
    }
    return render(request, 'jampelajaran_admin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def formjamadmin(request):
    form = JamForm()
    if request.method == 'POST':
        formsimpan = JamForm(request.POST)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('jampelajaran')
    context = {
        'judul': 'Form Jam Pelajaran',
        'menu': 'Jam Pelajaran',
        'form':form
    }
    return render(request, 'formjamadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def editjamadmin(request, pk):
    jam = Jam_pelajaran.objects.get(id=pk)
    form = JamForm(instance=jam)
    if request.method == 'POST':
        formsimpan = JamForm(request.POST, instance=jam)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('jampelajaran')
    context = {
        'judul': 'Formedit Jam Pelajaran',
        'menu': 'Jam Pelajaran',
        'form':form
    }
    return render(request, 'formjamadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def deletejamadmin(request, pk):
    hapus = Jam_pelajaran.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('jampelajaran')

    context = {
        'judul': 'Hapus Jam Pelajaran',
        'menu': 'Jam Pelajaran',
        'hapus':hapus  
    }
    return render(request, 'hapusjamadmin.html', context)


@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def settinggaji(request):
    settinggaji = Setting_gaji.objects.all().order_by('-id')
    context = {
        'judul': 'Halaman Setting Gaji',
        'menu': 'Setting Gaji',
        'data':settinggaji,
    }
    return render(request, 'settinggaji_admin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def formsettinggajiadmin(request):
    form = SettingForm()
    if request.method == 'POST':
        formsimpan = SettingForm(request.POST)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('settinggaji')
    context = {
        'judul': 'Form Setting Gaji',
        'menu': 'Setting Gaji',
        'form':form
    }
    return render(request, 'formsettinggajiadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def editsettinggajiadmin(request, pk):
    settinggaji = Setting_gaji.objects.get(id=pk)
    form = SettingForm(instance=settinggaji)
    if request.method == 'POST':
        formsimpan = SettingForm(request.POST, instance=settinggaji)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('settinggaji')
    context = {
        'judul': 'Formedit Setting Gaji',
        'menu': 'Setting Gaji',
        'form':form
    }
    return render(request, 'formsettinggajiadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def deletesettinggajiadmin(request, pk):
    hapus = Setting_gaji.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('settinggaji')

    context = {
        'judul': 'Hapus Setting Gaji',
        'menu': 'Setting Gaji',
        'hapus':hapus  
    }
    return render(request, 'hapussettinggajiadmin.html', context)
@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def piketadmin(request):
    piket = Piket.objects.all()
    context = {
        'data': piket,
        'judul': 'Halaman Piket',
        'menu': 'Piket',
    }
    return render(request, 'piketadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def formpiketadmin(request):
    form = PiketForm()
    formuser = UserForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
       

        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.is_active = True
        user.save()

        akses = Group.objects.get(name='piket')
        user.groups.add(akses)

        formsimpan = PiketForm(request.POST)
        if formsimpan.is_valid():
            data = formsimpan.save()
            data.user = user
            data.save()
            return redirect('piketadmin')
    context = {
        'judul': 'Form Piket',

        'menu': 'Piket',
        'form':form,
        'formuser':formuser
    }
    return render(request, 'formpiketadmin.html', context)


@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def editpiketadmin(request, pk):
    piket = Piket.objects.get(id=pk)
    user = User.objects.get(id=piket.user.id)
    form = PiketForm(instance=piket)
    formuser = UserForm(instance=user)
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        if password:
            formsimpan = PiketForm(request.POST,request.FILES, instance=piket)
            simpanuser = User.objects.get(id=piket.user.id)
            simpanuser.set_password(password)
            simpanuser.username = username
            simpanuser.save()
            if formsimpan.is_valid():
                formsimpan.save()
                return redirect('piketadmin')
        else:
            formsimpan = PiketForm(request.POST,request.FILES, instance=piket)
            simpanuser = User.objects.get(id=piket.user.id)
            simpanuser.username = username
            simpanuser.save()
            if formsimpan.is_valid():
                formsimpan.save()
                return redirect('piketadmin')
    context = {
        'judul': 'Formedit Piket',

        'menu': 'Piket',
        'form':form,
        'formuser':formuser,
        'id': piket,
    }
    return render(request, 'formeditpiketadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def deletepiketadmin(request, pk):
    hapus = Piket.objects.get(id=pk)
    user = User.objects.get(id=hapus.user.id)
    if request.method == 'POST':
        hapus.delete()
        user.delete()
        return redirect('piketadmin')
    context = {
       'judul': 'Hapus Piket',

        'menu': 'Piket',
        'hapus':hapus,  
    }
    return render(request, 'hapuspiketadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def guruadmin(request):
    guru = Guru.objects.all()
    context = {
        'data': guru,
        'judul': 'Halaman Guru',
        'menu': 'Guru',
    }
    return render(request, 'guruadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def formguruadmin(request):
    form = GuruForm()
    formuser = UserForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
       
        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.is_active = True
        user.save()

        akses = Group.objects.get(name='guru')
        user.groups.add(akses)

        formsimpan = GuruForm(request.POST)
        if formsimpan.is_valid():
            data = formsimpan.save()
            data.user = user
            data.save()
            return redirect('guruadmin')
    context = {
        'judul': 'Form Guru',

        'menu': 'Guru',
        'form':form,
        'formuser':formuser
    }
    return render(request, 'formguruadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def editguruadmin(request, pk):
    guru = Guru.objects.get(id=pk)
    user = User.objects.get(id=guru.user.id)
    form = GuruForm(instance=guru)
    formuser = UserForm(instance=user)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if password:
            formsimpan = GuruForm(request.POST,request.FILES, instance=guru)
            simpanuser = User.objects.get(id=guru.user.id)
            simpanuser.set_password(password)
            simpanuser.username = username
            simpanuser.save()
            if formsimpan.is_valid():
                formsimpan.save()
                return redirect('guruadmin')
        else:
            formsimpan = GuruForm(request.POST,request.FILES, instance=guru)
            simpanuser = User.objects.get(id=guru.user.id)
            simpanuser.username = username
            simpanuser.save()
            if formsimpan.is_valid():
                formsimpan.save()
                return redirect('guruadmin')
    context = {
        'judul': 'Formedit Guru',
        'menu': 'Guru',
        'form':form,
        'formuser':formuser,
        'id': guru,
    }
    return render(request, 'formeditguruadmin.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def deleteguruadmin(request, pk):
    hapus = Guru.objects.get(id=pk)
    user = User.objects.get(id=hapus.user.id)
    if request.method == 'POST':
        hapus.delete()
        user.delete()
        return redirect('guruadmin')
    context = {
       'judul': 'Hapus Guru',

        'menu': 'Guru',
        'hapus':hapus,  
    }
    return render(request, 'hapusguruadmin.html', context)


def get_month_name(month_number):
    months = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    return months[month_number - 1] if 1 <= month_number <= 12 else ""


@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def gajiadmin(request):
    tahun_pelajaran_id = request.GET.get('tahun_pelajaran')
    guru_id = request.GET.get('guru')
    bulan = request.GET.get('bulan')

    queryset = Detail_gaji.objects.all()
    
    if tahun_pelajaran_id:
        queryset = queryset.filter(tahun_pelajaran_id=tahun_pelajaran_id)
    
    if guru_id:
        queryset = queryset.filter(guru_id=guru_id)
    
    if bulan:
        queryset = queryset.filter(tanggal__month=bulan)

    queryset = queryset.values(
        'tahun_pelajaran__nama',
        'tahun_pelajaran__id',
        'guru__nama_guru',
        'guru__id',
        'tanggal__month',
    ).annotate(
        month=ExtractMonth('tanggal'),
        total_nominal=Sum('nominal')
    ).order_by(
        'tahun_pelajaran__nama',
        'guru__nama_guru',
        'month'
    )

    for entry in queryset:
        entry['month_name'] = get_month_name(entry['month'])
        
    context = {
        'data': queryset,
        'tahun_pelajarans': Tahun_pelajaran.objects.all(),
        'gurus': Guru.objects.all(),
        'selected_tahun_pelajaran': tahun_pelajaran_id,
        'selected_guru': guru_id,
        'selected_bulan': bulan,
        'bulan_choices': [(str(i), get_month_name(i)) for i in range(1, 13)],
        'judul': 'Halaman Data Gaji',
        'menu': 'Gaji',
    }
    return render(request, 'gajiadmin.html', context)





@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def detailgajiadmin(request, th, guru, bulan):
   
    idtahun = Tahun_pelajaran.objects.get(id=th)
    idguru = Guru.objects.get(id=guru)
    namabulan = get_month_name(int(bulan))
   
    data = Detail_gaji.objects.filter(tahun_pelajaran=th, guru=guru,tanggal__month=bulan)
    context = {
        'judul': 'Detail Gaji Guru',
        'menu': 'Rincian Gaji Guru',
        'data':data,
        'idtahun':idtahun,
        'idguru':idguru,
        'namabulan':namabulan
        
      
    }
    return render(request, 'tampildetailgaji.html', context)

@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def editdetailgajiadmin(request, pk):
    detail = Detail_gaji.objects.get(id=pk)
    form = DetailForm(instance=detail)
    if request.method == 'POST':
        formsimpan = DetailForm(request.POST, instance=detail)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('detailgajiadmin', detail.tahun_pelajaran.id, detail.guru.id, detail.tanggal.month)
    context = {
        'judul': 'Edit Gaji Guru',
        'menu': 'Rincian Gaji Guru',
        'form':form,
        'detail':detail
    }
    return render(request, 'editdetailgajiadmin.html', context)


@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def deletedetailgajiadmin(request, pk):
    hapus = Detail_gaji.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('detailgajiadmin', hapus.tahun_pelajaran.id, hapus.guru.id, hapus.tanggal.month)

    context = {
         'judul': 'Hapus Gaji Guru',
        'menu': 'Rincian Gaji Guru',
        'hapus':hapus  
    }
    return render(request, 'deletedetailgajiadmin.html', context)
@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def laporanadmin(request):
    tahun_pelajaran_id = request.GET.get('tahun_pelajaran')
    guru_id = request.GET.get('guru')
    bulan = request.GET.get('bulan')

    queryset = Detail_gaji.objects.all()
    
    if tahun_pelajaran_id:
        queryset = queryset.filter(tahun_pelajaran_id=tahun_pelajaran_id)
    
    if guru_id:
        queryset = queryset.filter(guru_id=guru_id)
    
    if bulan:
        queryset = queryset.filter(tanggal__month=bulan)

    queryset = queryset.values(
        'tahun_pelajaran__nama',
        'tahun_pelajaran__id',
        'guru__nama_guru',
        'guru__id',
        'tanggal__month',
    ).annotate(
        month=ExtractMonth('tanggal'),
        total_nominal=Sum('nominal')
    ).order_by(
        'tahun_pelajaran__nama',
        'guru__nama_guru',
        'month'
    )

    for entry in queryset:
        entry['month_name'] = get_month_name(entry['month'])
        
    context = {
        'data': queryset,
        'tahun_pelajarans': Tahun_pelajaran.objects.all(),
        'gurus': Guru.objects.all(),
        'selected_tahun_pelajaran': tahun_pelajaran_id,
        'selected_guru': guru_id,
        'selected_bulan': bulan,
        'bulan_choices': [(str(i), get_month_name(i)) for i in range(1, 13)],
        'judul': 'Halaman Laporan Gaji',
        'menu': 'Laporan',
    }
    return render(request, 'laporanadmin.html', context)


@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def cetak_laporan_pdf(request):
    tahun_pelajaran_id = request.GET.get('tahun_pelajaran')
    guru_id = request.GET.get('guru')
    bulan = request.GET.get('bulan')

    queryset = Detail_gaji.objects.all()

    if tahun_pelajaran_id and tahun_pelajaran_id != '':
        queryset = queryset.filter(tahun_pelajaran_id=tahun_pelajaran_id)

    if guru_id and guru_id != '':
        queryset = queryset.filter(guru_id=guru_id)

    if bulan and bulan != '':
        queryset = queryset.filter(tanggal__month=bulan)

    queryset = queryset.values(
        'tahun_pelajaran__nama',
        'tahun_pelajaran__id',
        'guru__nama_guru',
        'guru__id',
        'tanggal__month',
    ).annotate(
        month=ExtractMonth('tanggal'),
        total_nominal=Sum('nominal')
    ).order_by(
        'tahun_pelajaran__nama',
        'guru__nama_guru',
        'month'
    )

    # Hitung total keseluruhan
    total_keseluruhan = queryset.aggregate(total=Sum('total_nominal'))['total'] or 0

    # Konversi angka bulan menjadi nama bulan
    for entry in queryset:
        entry['month_name'] = get_month_name(entry['month'])

    context = {
        'data': queryset,
        'tahun_pelajarans': Tahun_pelajaran.objects.all(),
        'gurus': Guru.objects.all(),
        'selected_tahun_pelajaran': tahun_pelajaran_id,
        'selected_guru': guru_id,
        'selected_bulan': bulan,
        'bulan_choices': [(str(i), get_month_name(i)) for i in range(1, 13)],
        'judul': 'Laporan Gaji PDF',
        'menu': 'Laporan',
        'total_keseluruhan': total_keseluruhan,  # Total keseluruhan dikirim ke template
    }

    # Render the template to HTML
    template_path = 'laporanadmin_pdf.html'
    template = get_template(template_path)
    html = template.render(context)

    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="laporan_gaji.pdf"'

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(
        html, dest=response
    )

    # If error then show some message
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
def get_nama_bulan(bulan):
    bulan_dict = {
        1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
        5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
        9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
    }
    return bulan_dict.get(bulan, '')
@login_required(login_url='halamanlogin')
@ijinkan_pengguna(yang_diizinkan=['administrator'])
def cetak_slip_gaji(request, guru_id, bulan):
    guru = get_object_or_404(Guru, pk=guru_id)
    detail_gaji = Detail_gaji.objects.filter(guru=guru, tanggal__month=bulan)
    
    total_nominal = detail_gaji.aggregate(total=Sum('nominal'))['total'] or 0
    # Mengambil tahun pelajaran dari entri pertama di gaji
    if detail_gaji.exists():
        tahun_pelajaran = detail_gaji.first().tahun_pelajaran
    else:
        tahun_pelajaran = None
        
    nama_bulan = get_nama_bulan(int(bulan))
    context = {
        'guru': guru,
        'detail_gaji': detail_gaji,
        'bulan': bulan,
        'total_nominal': total_nominal,
        'bulan': nama_bulan,
        'tahun_pelajaran': tahun_pelajaran,
    }

    template_path = 'slip_gaji.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="slip_gaji.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
