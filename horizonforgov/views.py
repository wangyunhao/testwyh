# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response,render,get_object_or_404  
from django.http import HttpResponse, HttpResponseRedirect  
from django.contrib.auth.models import User  
from django.contrib import auth
from django.contrib import messages
from django.template.context import RequestContext
from django.shortcuts import redirect
from django.forms.formsets import formset_factory
#from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from bootstrap_toolkit.widgets import BootstrapUneditableInput
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template.loader import get_template

from forms import LoginForm, PropertyForm
from models import Property, Availability, Tenant

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from models import UserRole
################
#userDemo
def userrole(request):  
    desc = User.objects.all()[0].get_profile().description  
    return HttpResponse(desc) 


#Expand Redirct Here
def index(request):
    return redirect(reverse(login))
#  


#Login 
def login(request):

    if request.method == 'GET':
        if request.user.is_authenticated():
            return render_to_response('#.html', RequestContext(request))
        else:
            form = LoginForm()
            return render_to_response('user/login.html', RequestContext(request, {'form': form,}))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return render_to_response('#.html', RequestContext(request))
            else:
                return render_to_response('user/login.html', RequestContext(request, {'form': form,'password_is_wrong':True, 'errors': u'登录失败，请检查登录信息'}))
        else:
            return render_to_response('user/login.html', RequestContext(request, {'form': form, 'input_is_wrong':True, 'errors': u'请正确输入登录信息'}))
 
 
 
@login_required          
def dashboard(request):
    return render_to_response('#.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse(login))
    

#   



#Property Related Views 


@login_required
def view_property(request):
    
    #For Property Delete
    if request.method == 'POST' and request.GET.get('id'):
        property_queried = Property.objects.filter(Property.id == request.GET.get('id')).first()
        Availability.objects.filter(Property=property_queried).delete()
        property_queried.delete()
    #
    
    #For Property Search 
    if request.GET.get('search'):
        keyword_searched = request.GET.get('search')
        properties = Property.objects.filter(Q(NameUnicode__icontains=keyword_searched) | Q(AddressLine1__icontains=keyword_searched))
    else:
        keyword = None
        properties = Property.objects.all()

        
    properties = properties.order_by('NameUnicode')
    
    return render_to_response('property/view.html', {'properties': properties}, context_instance = RequestContext(request))    
'''    page_properties=Paginator(properties,limit)s
    page_properties_review=Paginator(properties,limit)
    page=request.GET.get('page')
    table=request.GET.get('table','none')
    try:
        if table=='1':
            properties=page_properties.page(page)
        else:s
            properties=page_properties.page(1)
    except PageNotAnInteger:
        properties=page_properties.page(1)
    except EmptyPage:
        properties=page_properties.page(page_properties.num_pages)
    try:
        if table=='2':
            properties_review=page_properties_review.page(page)
        else:
            properties_review=page_properties_review.page(1)
    except PageNotAnInteger:
        properties_review=page_properties_review.page(1)
    except EmptyPage:
        properties_review=page_properties_review.page(page_properties_review.num_pages)
    return render_to_response('property/view.html',{'properties':properties,'properties_review':properties_review},context_instance=RequestContext(request))
'''    
    #
    

 

@login_required
def add_property(request):
    form = PropertyForm()
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_to_add = Property(form.cleaned_data)
            instance = form.save()
            
    return render_to_response('property/add.html', {'form': form}, context_instance = RequestContext(request))
'''            if request.files:
                if 'Image' in request.files and request.files['Image']:
    
                    image = request.files['Image']
                    new_property.ImageId = images.save(image, name=str(new_property.Name) + "_image." + image.filename.split('.')[-1].lower())
    
                if 'Document' in request.files and request.files['Document']:
    
                    document = request.files['Document']
                    new_property.DocumentId = documents.save(document, name=str(new_property.Name) + "_doc." + document.filename.split('.')[-1].lower())
                db.session.commit()
'''
#            flash('数据已被成功记录')

    #


'''  
@app.route('/dashboard/property/delete/<int:iden>', methods = ['POST'])
@login_required
def delete_property(iden):
    if iden:
        prop = Property.query.filter(Property.Id == iden).first()
        availabilities = prop.Availability
        if prop.ImageId:
            os.remove(os.path.abspath(os.path.dirname(__file__)) + '/uploads/images/' + prop.ImageId)
        if prop.DocumentId:
            os.remove(os.path.abspath(os.path.dirname(__file__)) + '/uploads/documents/' + prop.DocumentId)
        db.session.delete(prop)
        for availability in availabilities:
            db.session.delete(availability)
        db.session.commit()

    return redirect(url_for('view_property'))
    

@app.route('/dashboard/property/image/<filename>')
@login_required 
def get_image(filename):
    if not filename:
        abort(404)
    return send_file('uploads/images/' + filename)

@app.route('/dashboard/property/doc/<filename>')
@login_required 
def get_doc(filename):
    if not filename:
        abort(404)
    return send_file('uploads/documents/' + filename)
    

@app.route('/dashboard/property/edit/<int:iden>', methods = ['POST', 'GET'])
@login_required
def edit_property(iden):
    if not iden:
        redirect(url_for('view_property'))
    prop = Property.query.filter(Property.Id==iden).first()
    if prop == None:
        abort(404)
        
    if request.method == 'POST':
        form = PropertyForm(request.form, obj=prop)
        if form.validate_on_submit():
            form.populate_obj(prop)
            if request.files:
                if 'Image' in request.files and request.files['Image']:
                    if prop.ImageId:
                        os.remove(os.path.abspath(os.path.dirname(__file__)) + '/uploads/images/' + prop.ImageId)
                    image = request.files['Image']
                    prop.ImageId = images.save(image, name=str(prop.Name) + "_image." + image.filename.split('.')[-1].lower())
                    
                if 'Document' in request.files and request.files['Document']:
                    if prop.DocumentId:
                        os.remove(os.path.abspath(os.path.dirname(__file__)) + '/uploads/documents/' + prop.DocumentId)
                    document = request.files['Document']
                    prop.DocumentId = documents.save(document, name=str(prop.Name) + "_doc." + document.filename.split('.')[-1].lower())
                
                db.session.commit() 
            prop = Property.query.filter(Property.Id==iden).first()
            flash('数据已被成功记录')
            
    form = PropertyForm()
    form.process(obj=prop)
    form.data['Image'] = prop.ImageId
    form.data['Document'] = prop.DocumentId
    return html_minify(render_template('property/add.html',
                           user=g.user, form=form))

                           
@app.route('/dashboard/availability/add', methods = ['GET'])
@login_required
def display_availability():
    if request.args.get('search'):
        keyword = request.args.get('search')
        properties = Property.query.filter(or_(Property.Name.contains(keyword), Property.NameUnicode.contains(keyword), Property.AddressLine1.contains(keyword)))
    else:
        keyword = None
        properties = Property.query
        
    if request.args.get('page'):
        page = request.args.get('page')
    else:
        page = 1
        
    properties = properties.order_by(Property.Name).paginate(page=int(page), per_page=10)
    return html_minify(render_template('availability/view_property_list.html', properties=properties, keyword=keyword, mode='add'))

@app.route('/dashboard/availability/add/<int:iden>', methods = ['GET', 'POST'])
@login_required
def add_availability(iden=None):
    if iden == None:
        return redirect(url_for('display_availability'))
    prop = Property.query.filter(Property.Id==iden).first()
    if prop == None:
        abort(404)
        
    form = AvailabilityForm()
    if request.method == 'POST':


        if form.validate_on_submit() and request.method == 'POST':
            new_availability = Availability(Area=0.0)
            form.populate_obj(new_availability)
            new_availability.Property = prop
            db.session.add(new_availability)
            print "a"
            db.session.commit()
            print "c"
            form = AvailabilityForm()
            print "d"
            return redirect(url_for('display_availability'))
            print "e"
    return html_minify(render_template('availability/add.html', form=form))
    
    
@app.route('/dashboard/availability/view', methods = ['GET'])
@login_required
def view_availability():
    if request.args.get('search'):
        keyword = request.args.get('search')
        properties = Property.query.filter(or_(Property.Name.contains(keyword), Property.NameUnicode.contains(keyword), Property.AddressLine1.contains(keyword)))
    else:
        keyword = None
        properties = Property.query
        
    if request.args.get('page'):
        page = request.args.get('page')
    else:
        page = 1
        
    properties = properties.order_by(Property.Name).paginate(page=int(page), per_page=10)
    return html_minify(render_template('availability/view_property_list.html', properties=properties, keyword=keyword, mode='view'))
   
    
@app.route('/dashboard/availability/view/<int:iden>', methods = ['GET', 'POST'])
@login_required
def view_availability_list(iden = None):
    if iden == None:
        redirect(url_for('view_availability'))
        
    if request.args.get('search'):
        keyword = request.args.get('search')
        availabilities = Availability.query.filter(and_(Availability.PropertyId == iden,or_(Availability.Floor.contains(keyword), Availability.Unit.contains(keyword),
                                                                                          Availability.Status.contains(keyword), Availability.Area.contains(keyword))))
    else:
        keyword = None
        availabilities = Availability.query.filter(Availability.PropertyId == iden)
   
    if request.args.get('page'):
        page = request.args.get('page')
    else:
        page = 1
    
    availabilities = availabilities.order_by(Availability.Floor).paginate(page=int(page), per_page=10)
    
    return html_minify(render_template('availability/view_availability_list.html', availabilities=availabilities, keyword=keyword))


@app.route('/dashboard/availability/delete/<int:iden>', methods = ['POST'])
@login_required
def delete_availability(iden = None):
    if iden == None:
        redirect(url_for('view_availability'))
        
    availability = Availability.query.filter(Availability.Id == iden).first()
    
    db.session.delete(availability)
    db.session.commit()
        
    return redirect(url_for('view_availability_list', iden=iden))                                          

@app.route('/dashboard/availability/edit/<int:iden>', methods = ['POST', 'GET'])
@login_required
def edit_availability(iden=None):
    if not iden:
        redirect(url_for('view_availability'))
    availability = Availability.query.filter(Availability.Id==iden).first()
    if availability == None:
        abort(404)
        
    if request.method == 'POST':
        form = AvailabilityForm(request.form, obj=availability)
        if form.validate_on_submit():
            flash('Entry was successfully edited')
            form.populate_obj(availability)
            db.session.commit()
            availability = Availability.query.filter(Availability.Id==iden).first()
            
    form = AvailabilityForm()
    form.process(obj=availability)

    return html_minify(render_template('availability/add.html',
                           user=g.user, form=form))
                           
                           
                           
@app.route('/dashboard/tenant/add', methods = ['POST', 'GET'])
@login_required
def add_tenant():
    form = TenantForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_tenant = Tenant(TenantName="Temp")
            form.populate_obj(new_tenant)
            db.session.add(new_tenant)
            db.session.commit()
#            if request.files:
#                if 'Image' in request.files and request.files['Image']:
#    
#                    image = request.files['Image']
#                    new_property.ImageId = images.save(image, name=str(new_property.Name) + "_image." + image.filename.split('.')[-1].lower())
#    
#                if 'Document' in request.files and request.files['Document']:
#    
#                    document = request.files['Document']
#                    new_property.DocumentId = documents.save(document, name=str(new_property.Name) + "_doc." + document.filename.split('.')[-1].lower())
#                db.session.commit()

            flash('数据已被成功记录')
    return html_minify(html_minify(render_template('tenant/add.html',
                           user=g.user, form=form)))


@app.route('/dashboard/tenant/view', methods = ['GET', 'POST'])
@login_required
def view_tenant():
    if request.method == 'POST' and request.args.get('id'):
        prop = Tenant.query.filter(Tenant.Id == request.args.get('id')).first()
        tenants = prop.Tenant
        db.session.delete(prop)
#        for tenant in tenants:
#            db.session.delete(tenant)
        db.session.commit()
        
    if request.args.get('search'):
        keyword = request.args.get('search')
        tenants = Tenant.query.filter(or_(Tenant.TenantName.contains(keyword), Tenant.TenantType.contains(keyword), Tenant.TenantStatus.contains(keyword)))
    else:
        keyword = None
        tenants = Tenant.query
        
    if request.args.get('page'):
        page = request.args.get('page')
    else:
        page = 1
        
    tenants = tenants.order_by(Tenant.TenantName).paginate(page=int(page), per_page=10)

    return html_minify(render_template('tenant/view.html', tenants=tenants, keyword=keyword))
    
@app.route('/dashboard/tenant/delete/<int:iden>', methods = ['POST'])
@login_required
def delete_tenant(iden):
    if iden:
        prop = Tenant.query.filter(Tenant.Id == iden).first()
#        availabilities = prop.Availability
#        if prop.ImageId:
#            os.remove(os.path.abspath(os.path.dirname(__file__)) + '/uploads/images/' + prop.ImageId)
#        if prop.DocumentId:
#            os.remove(os.path.abspath(os.path.dirname(__file__)) + '/uploads/documents/' + prop.DocumentId)
        db.session.delete(prop)
#        for availability in availabilities:
#            db.session.delete(availability)
        db.session.commit()

    return redirect(url_for('view_tenant'))
    
@app.route('/dashboard/tenant/edit/<int:iden>', methods = ['POST', 'GET'])
@login_required
def edit_tenant(iden):
    if not iden:
        redirect(url_for('view_tenant'))
    prop = Tenant.query.filter(Tenant.Id==iden).first()
    if prop == None:
        abort(404)
        
    if request.method == 'POST':
        form = TenantForm(request.form, obj=prop)
        if form.validate_on_submit():
            form.populate_obj(prop)
#            if request.files:
#                if 'Image' in request.files and request.files['Image']:
#                    if prop.ImageId:
#                        os.remove(os.path.abspath(os.path.dirname(__file__)) + '/uploads/images/' + prop.ImageId)
#                    image = request.files['Image']
#                    prop.ImageId = images.save(image, name=str(prop.Name) + "_image." + image.filename.split('.')[-1].lower())
#                    
#                if 'Document' in request.files and request.files['Document']:
#                    if prop.DocumentId:
#                        os.remove(os.path.abspath(os.path.dirname(__file__)) + '/uploads/documents/' + prop.DocumentId)
#                    document = request.files['Document']
#                    prop.DocumentId = documents.save(document, name=str(prop.Name) + "_doc." + document.filename.split('.')[-1].lower())
                
            db.session.commit() 
            prop = Tenant.query.filter(Tenant.Id==iden).first()
            flash('数据已被成功记录')
            
    form = TenantForm()
    form.process(obj=prop)
#    form.data['Image'] = prop.ImageId
#    form.data['Document'] = prop.DocumentId
    return html_minify(render_template('tenant/add.html',
                           user=g.user, form=form))
'''