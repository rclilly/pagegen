from pagegen.utility import DIRDEFAULTFILE, appropriate_markup, generate_menu, CONTENTDIR, ASSETDIR
from os.path import isfile, getctime
from os import makedirs
from PIL import Image, ImageOps
from hashlib import md5


def built_in_youtube(site, page, video_id, width=420, height=315):

	html = '<iframe width="420" height="315" src="https://www.youtube.com/embed/' + video_id + '"></iframe>'

	return appropriate_markup(page, html)


def built_in_figure(site, page, caption, alternative_text, src_path):
	''' Make html figure '''

	html = '<figure>\n'
	html += '<img src="' + src_path + '" alt="' + alternative_text + '">\n'
	html += '<figcaption>' + caption + '</figcaption>\n'
	html += '</figure>\n'

	return appropriate_markup(page, html)


def built_in_page_url(site, page, page_path):
	''' Return url to page, taking into account if default extension '''

	for p in site.page_list:
		if p.url_path.endswith('/'):
			url_path = p.url_path + DIRDEFAULTFILE + site.default_extension
		else:
			url_path = p.url_path

		if url_path == page_path or url_path == page_path + site.default_extension:
			return url_path

	raise Exception('No page matches "' + page_path + '"')


def built_in_menu(site, page):
	''' Generate fully recursive site menu '''
	generate_menu(site.pages, page)
	return page.menu


def built_in_gravatar(site, page, email, name, size):
	''' Return gravatar img tag '''

	email_hash = md5(email.encode())
	email_hash = email_hash.hexdigest()

	html = '<img src="https://www.gravatar.com/avatar/' + email_hash + '" alt="' + name + '" width="' + size + '" height="' + size + '" />'

	return html


def built_in_image(site, page, image_source, alt_attribute, target_dir=None, image_class=None, image_size=None):
	''' Return img tag and optionally resize image using image_class settings from site.conf or image_size(XxY) argument. Maintains aspect ration by cropping with center gravity and resize to dimensions '''

	resize = False

	# Path cannot start with .
	if image_source.startswith('.'):
		raise Exception('Image source cannot start with .')

	# If path is relative, prefix with site_dir
	if not image_source.startswith('/'):
		image_source = site.site_dir + '/' + image_source

	# Check source image exists
	if not isfile(image_source):
		raise Exception('No file: ' + source_image)

	t = image_source.rpartition('/')
	source_dir = t[0]
	source_file = t[2]

	# Target dir defults to assets
	if target_dir is None:
		target_dir = site.asset_dir 
	else:
		# Target dir cannot start with .
		if target_dir.startswith('.'):
			raise Exception('target_dir cannot start with .')

		# Target_dir is always relative to asset dir
		if target_dir.startswith('/'):
			target_dir = site.asset_dir + target_dir
		else:
			target_dir = site.asset_dir + '/' + target_dir

	# Lookup class settings if image_class argument
	if image_class:
		width = site.image_classes[image_class]['width']
		height = site.image_classes[image_class]['height']
		target_file = source_file.replace('.', '-' + image_class + '.')
		resize = True
	elif image_size:
		dims = image_size.split('x')
		target_file = source_file.replace('.', '-' + image_size + '.')

		if len(dims) != 2:
			raise Exception('Unable to parse WidthxHeight: ' + image_size)

		width = int(dims[0])
		height = int(dims[1])
		resize = True
	else:
		target_file = source_file
		resize = False

	# Image src
	length_content_dir_path = len(site.site_dir + '/' + CONTENTDIR)
	img_src = site.base_url + target_dir[length_content_dir_path:] + '/' + target_file

	# Create target dir if needed
	makedirs(target_dir, exist_ok=True)

	target_file_path = target_dir + '/' + target_file

	#If image already exists, check if source is newer than target, else is target has correct dimensions, failing all that then resize
	create_target = False
	if isfile(target_file_path):
		if getctime(target_file_path) < getctime(image_source):
			create_target = True
	else:
		create_target = True

	if create_target:
		im = Image.open(image_source)	
		im_new = ImageOps.fit(im, (width, height))
		im_new.save(target_file_path)

	html = '<img src="' + img_src + '" alt="' + alt_attribute + '" width="' + str(width) + '" height="' + str(height) + '" />'

	return appropriate_markup(page, html)


def built_in_list_authors(site, page):
	''' List authors '''

	for author in page.authors:
		if 'name' in author.keys():
			name = author['name']
		else:
			name = author['id']

		html = '<li><a href="' + author['author_page'] + '">' + name + '</a></li>'

	html = '<ol>' + html + '</ol>'

	return appropriate_markup(page, html)


def built_in_more(site, page):
	''' Adds <!-- more --> comment to html output, for use with excerpts '''
	return appropriate_markup(page, '<!-- more -->')

