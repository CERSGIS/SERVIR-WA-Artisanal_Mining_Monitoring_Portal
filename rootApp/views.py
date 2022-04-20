from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from djgeojson.views import GeoJSONLayerView
from .models import *
from django.contrib.auth import authenticate
import ee
from datetime import datetime, date


from datetime import date

today1 = date.today()

# dd/mm/YY
today = today1.strftime("%Y-%m-%d")
# Create your views here.
# def login_view(request):
# 	request.session["next"] = request.GET.get("next")
# 	if request.method == "POST":
# 		username = request.POST.get("user", "")
# 		password = request.POST.get("pass", "")
# 		user = authenticate(username=username, password=password)
# 		if user:
# 			login(request, user)
# 			if request.session["next"]:
# 				return redirect(request.session["next"])
# 			else:
# 				return redirect("/backend/")
# 	return render(request, "rootApp/login_form.html", locals())


def root_view(request):
	toHTML = {}
	year = datetime.now().year

	return render(request, 'rootApp/index.html', locals())


def about_view(request):
	toHTML = {}
	return render(request, 'rootApp/about.html', toHTML)


def loaddef():
	try:

		ee.Initialize()
	except Exception as e:
		credentials = ee.ServiceAccountCredentials(
			'geeresearch@geeapp-1577771889447.iam.gserviceaccount.com', 'geeapp-1577771889447-dd8ab00048c7.json')
		ee.Initialize(credentials)


def addIDfunc(feature):
	return feature.set({"id": 1})


def bufferfunc(feature):
	return feature.buffer(40)


def swap(array):
	array[0], array[1] = array[1], array[0]
	return array


def getdata_view(request):
	toHTML = {}
	try:
		loaddef()

		dataset = computeSentinel(
			request.GET.get("from"), request.GET.get("to"))

		if request.GET.get("color"):
			styling = {'min': 0, 'max': 1, 'palette': [
				str(request.GET.get("color"))]}
		else:
			styling = {'min': 0, 'max': 1, 'palette': ['red']}

		try:
			idfeatures = dataset.getMapId(styling)

			toHTML['mapid'] = str(idfeatures['tile_fetcher'].url_format)
			toHTML['token'] = idfeatures['token']
		except Exception as e:

			toHTML['mapid'] = 'no_image'
			# raise e
			# return  HttpResponse("fail")

		# idfeatures = dataset.getMapId(styling)

	except Exception as e:

		toHTML['mapid'] = 'error'
		# raise e

	return JsonResponse(toHTML, safe=False)




class RegionView(GeoJSONLayerView):
  model = Region
  precision = 4
  simplify = 0.001
  properties = ('region',"reg_code")


class DistrictView(GeoJSONLayerView):
  model = District
  precision = 4
  simplify = 0.001
  properties = ('district',"district_code")


class ProtectedAreaView(GeoJSONLayerView):
  model = ProtectedArea
  precision = 4
  simplify = 0.001
  properties = ('reserve_na',"area_sqkm")


  
# def timeseries_view(request):
# 	toHTML={}
# 	try:
# 		loaddef()
# 		galamsey_aoi=ee.FeatureCollection("users/mamponsah91/Gala_pilarea")
# 		osm_settlement_dataset=ee.FeatureCollection("users/mamponsah91/osm_settlement")
# 		gala_set=ee.FeatureCollection("users/mamponsah91/gala_set")
# 		consolidated_mask=ee.FeatureCollection("users/mamponsah91/Consolidated_mask")
# 		table=ee.FeatureCollection("users/mamponsah91/gala_road_edit")
# 		gala_buffer=ee.FeatureCollection("users/mamponsah91/Gala_buffer")
# 		builtup=ee.Image("users/mamponsah91/set")


# 		sarCollection = ee.ImageCollection("COPERNICUS/S1_GRD")\
# 		.filterBounds(galamsey_aoi)\
# 		.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))\
# 		.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))\
# 		.filter(ee.Filter.eq('instrumentMode', 'IW'))\
# 		.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))\


# 		startyear=request.GET.get("from")
# 		endyear=request.GET.get("to")


# 		valuestored=[]
# 		yeardate=[]
# 		step  = 1
# 		stop  = int(endyear)
# 		start =int(startyear) #now stop is 6
# 		stop +=step #now stop is 6


# 		for year in range(start,stop,step):

# 			yeardate.append(year)
# 			print(year)
# 			print("ernest")


# 			datefrom=datetime.strptime(str(year)+"-1-1","%Y-%m-%d" )
# 			dateto=datetime.strptime(str(year)+"-12-31","%Y-%m-%d")
# 		if datefrom == dateto:
# 			sar=sarCollection\
# 			.filterDate(ee.Date(datefrom),ee.Date(dateto).advance(4, 'day'))\
# 			.mean()\
# 			.clip(galamsey_aoi)
# 			# print(sarCollection.size())
# 			# print(sarCollection.size())
# 		else:

# 			sar= sarCollection\
# 			.filterDate(ee.Date(datefrom),ee.Date(dateto))\
# 			.mean()\
# 			.clip(galamsey_aoi)\


# 			Quater = ee.Image.cat([
# 			sar.select('VV'),
# 			sar.select('VH').multiply(2).rename('DVH'),
# 			sar.select('VV').divide(sar.select('VH')).divide(100).rename('PVH')
# 			]);

# 			threshold = Quater.select('VV').gte(-20) and Quater.select('VV').lte(-10)

# 			# //Importing SENTINEL-2 collection
# 			St2 = ee.ImageCollection('COPERNICUS/S2')\
# 				.filterDate('2015-01-01','2020-07-15')\
# 				.filterBounds(galamsey_aoi)\
# 				.select(['B1','B2','B3','B4','B8','B9','B11','B12'])\
# 				  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',5))\
# 				  .median()\
# 				  .clip(galamsey_aoi);


# 			# // NDVI Composite
# 			ndvi = St2.normalizedDifference(['B8','B4']);

# 			ndvi1 = ndvi.gt(0.3).Not().selfMask();

# 			ndvi2 = ndvi.lte(0.018).And(ndvi.gt(-0.07));

# 			ndviFinal = ndvi2.blend(ndvi1).selfMask();


# 			# # // Map the ID function over the FeatureCollection and converting to Image (osm settlement).
# 			osm_settlement = osm_settlement_dataset.map(addIDfunc)\
# 								.reduceToImage(**{
# 								'properties':['id'],
# 								'reducer':ee.Reducer.first()
# 								}
# 								);
# 			# //Clipping osm_settlement to project area
# 			mask1 = osm_settlement.clip(galamsey_aoi)

# 			road_buffer = table.map(bufferfunc)

# 			road = road_buffer.map(addIDfunc)\
# 						.reduceToImage(**{
# 						"properties":['id'],
# 						"reducer":ee.Reducer.first()
# 						}
# 						);

# 	# //Merging or combining all the mask
# 			mask = mask1.blend(builtup).blend(road).mask().clip(galamsey_aoi).selfMask();

# 	# // Creating of final mask
# 			# maskComposite = ndviFinal.updateMask(mask.Not()).selfMask()
# 			maskComposite = ndviFinal.updateMask(mask.unmask().Not())


# 	# // Displaying and Visualizing after thresholding
# 			dataset = threshold.updateMask(maskComposite).clip(gala_buffer).selfMask();


# 			asd=request.GET.get("coords")

# 			if asd:
# 				a = asd.replace("(","[")
# 				b=a.replace(")","]")
# 				c=b.replace("LatLng" ,"")

# 				getbounds=eval('[' + c + ']')

# 				bound = [swap(aa) for aa in getbounds]

# 				poly=ee.Geometry.Polygon(bound)


# 				dataset = dataset.clip(poly);


# 			# if request.GET.get("download"):
# 				dataset = ee.Image(dataset);


# 			area = dataset.multiply(ee.Image.pixelArea()).divide(1000*1000);

# 			stat = area.reduceRegion (
# 				**{
# 			  'reducer': ee.Reducer.sum(),
# 			  'geometry': poly,
# 			  'crs':'EPSG:4326',
# 			  'scale': 30,
# 			  'maxPixels': 1e9
# 				});


# 			valuestored.append(stat.getInfo()['VV'])
# 			dd="{:.3f}".format(stat.getInfo()['VV'])
# 	except Exception as e:
# 		raise e
# 	print(valuestored)
# 	print(yeardate)
# 	return render(request, 'rootApp/chart.html', locals())


def datetime_range(start=None, end=None):
	span = end - start
	for i in range(span.days + 1):
		yield start + timedelta(days=i)


# def getImagedownload(request):
#     loaddef()

#     year = request.GET.get("year")[-4:]

#     asd = request.GET.get("coords")

#     if asd:
#         a = asd.replace("(", "[")
#         b = a.replace(")", "]")
#         c = b.replace("LatLng", "")

#         getbounds = eval('[' + c + ']')

#         bound = [swap(aa) for aa in getbounds]

#         poly = ee.Geometry.Polygon(bound)

#         class_image = ee.Image(
#             'users/mamponsah91/Galamsey'+str(year) + '_proj').select(0).clip(poly)

#         area = class_image.multiply(ee.Image.pixelArea()).divide(1000*1000)

#         stat = area.reduceRegion(
#             **{
#                 'reducer': ee.Reducer.sum(),
#                 'geometry': poly,
#                 'crs': 'EPSG:4326',
#                 'scale': 30,
#                 'maxPixels': 1e9
#             })

#         # print(stat.getInfo())

#         path = osm_settlement.getDownloadUrl({
#             'scale': 30,
#             'crs': 'EPSG:4326',
#             'region': bound
#         })

#         return HttpResponse(path)

def getImagedownload(request):
	loaddef()

  

	asd = request.GET.get("coords")

	if asd:
		a = asd.replace("(", "[")
		b = a.replace(")", "]")
		c = b.replace("LatLng", "")

		getbounds = eval('[' + c + ']')

		bound = [swap(aa) for aa in getbounds]

		poly = ee.Geometry.Polygon(bound)

	dataset = computeSentinel(
			request.GET.get("from"), request.GET.get("to"),asd)

	path = dataset.getDownloadUrl({
		'scale': 30,
		'crs': 'EPSG:4326',
		'region': bound
	})

	return HttpResponse(path)


	
# def computeSentinel(start,end):
# 	toHTML={}
# 	try:
# 		loaddef()
# 		galamsey_aoi=ee.FeatureCollection("users/mamponsah91/Gala_pilarea")
# 		osm_settlement_dataset=ee.FeatureCollection("users/mamponsah91/osm_settlement")
# 		gala_set=ee.FeatureCollection("users/mamponsah91/gala_set")
# 		consolidated_mask=ee.FeatureCollection("users/mamponsah91/Consolidated_mask")
# 		table=ee.FeatureCollection("users/mamponsah91/gala_road_edit")
# 		gala_buffer=ee.FeatureCollection("users/mamponsah91/Gala_buffer")
# 		builtup=ee.Image("users/mamponsah91/set")


# 		sarCollection = ee.ImageCollection("COPERNICUS/S1_GRD")\
# 		.filterBounds(galamsey_aoi)\
# 		.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))\
# 		.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))\
# 		.filter(ee.Filter.eq('instrumentMode', 'IW'))\
# 		.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))


# 		datefrom=datetime.strptime(start,"%Y-%m-%d" )
# 		dateto=datetime.strptime(end,"%Y-%m-%d")


# 		if datefrom == dateto:
# 			sar=sarCollection\
# 			.filterDate(ee.Date(datefrom),ee.Date(dateto).advance(1, 'day'))\
# 			.mean()\
# 			.clip(galamsey_aoi)

# 			print(sarCollection.toList(20).size())

# 		else:

# 			sar= sarCollection\
# 			.filterDate(ee.Date(datefrom),ee.Date(dateto))\
# 			.mean()\
# 			.clip(galamsey_aoi)\


# 		Quater = ee.Image.cat([
# 		sar.select('VV'),
# 		sar.select('VH').multiply(2).rename('DVH'),
# 		sar.select('VV').divide(sar.select('VH')).divide(100).rename('PVH')
# 		]);

# 		threshold = Quater.select('VV').gte(-20) and Quater.select('VV').lte(-10)


# 		# //Importing SENTINEL-2 collection
# 		St2 = ee.ImageCollection('COPERNICUS/S2')\
# 			.filterDate('2015-01-01','2020-07-15')\
# 			.filterBounds(galamsey_aoi)\
# 			.select(['B1','B2','B3','B4','B8','B9','B11','B12'])\
# 			  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',5))\
# 			  .median()\
# 			  .clip(galamsey_aoi);


# 		# // NDVI Composite
# 		ndvi = St2.normalizedDifference(['B8','B4']);

# 		ndvi1 = ndvi.gt(0.3).Not().selfMask();

# 		ndvi2 = ndvi.lte(0.018).And(ndvi.gt(-0.07));

# 		ndviFinal = ndvi2.blend(ndvi1).selfMask();


# 		# # // Map the ID function over the FeatureCollection and converting to Image (osm settlement).
# 		osm_settlement = osm_settlement_dataset.map(addIDfunc)\
# 							.reduceToImage(**{
# 							'properties':['id'],
# 							'reducer':ee.Reducer.first()
# 							}
# 							);

# 		# //Clipping osm_settlement to project area
# 		mask1 = osm_settlement.clip(galamsey_aoi)
# 		# buffer1 = bufferfunc()
# 		road_buffer = table.map(bufferfunc)

# 		road = road_buffer.map(addIDfunc)\
# 					.reduceToImage(**{
# 					"properties":['id'],
# 					"reducer":ee.Reducer.first()
# 					}
# 					);

# # //Merging or combining all the mask
# 		mask = mask1.blend(builtup).blend(road).mask().clip(galamsey_aoi).selfMask();

# # // Creating of final mask
# 		# maskComposite = ndviFinal.updateMask(mask.Not()).selfMask()
# 		maskComposite = ndviFinal.updateMask(mask.unmask().Not())


# # // Displaying and Visualizing after thresholding
# 		dataset = threshold.updateMask(maskComposite).clip(gala_buffer).selfMask();

# 		return dataset
# 	except Exception as e:
# 		raise e
# 		ass=None
# 		return ass

def computeSentinel(start, end, coords=None):
	toHTML = {}
	try:
		loaddef()
		galamsey_aoi = ee.FeatureCollection("users/mamponsah91/Gala_pilarea")
		osm_settlement_dataset = ee.FeatureCollection(
			"users/mamponsah91/osm_settlement")
		gala_set = ee.FeatureCollection("users/mamponsah91/gala_set")
		consolidated_mask = ee.FeatureCollection(
			"users/mamponsah91/Consolidated_mask")
		table = ee.FeatureCollection("users/mamponsah91/gala_road_edit")
		gala_buffer = ee.FeatureCollection("users/mamponsah91/Gala_buffer")
		road_network = ee.FeatureCollection("users/mamponsah91/Road_network")
		builtup = ee.Image("users/mamponsah91/set")

		sarCollection = ee.ImageCollection("COPERNICUS/S1_GRD")\
			.filterBounds(galamsey_aoi)\
			.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))\
			.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))\
			.filter(ee.Filter.eq('instrumentMode', 'IW'))\
			.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))\


		datefrom = datetime.strptime(start, "%Y-%m-%d")
		dateto = datetime.strptime(end, "%Y-%m-%d")

		if datefrom == dateto:

			if coords:
				a = coords.replace("(", "[")
				b = a.replace(")", "]")
				c = b.replace("LatLng", "")

				getbounds = eval('[' + c + ']')

				bound = [swap(aa) for aa in getbounds]

				poly = ee.Geometry.Polygon(bound)

				sar = sarCollection\
					.filterDate(ee.Date(datefrom), ee.Date(dateto).advance(12, 'day'))\
					.mean()\
					.clip(poly)
			else:

				sar = sarCollection\
					.filterDate(ee.Date(datefrom), ee.Date(dateto).advance(12, 'day'))\
					.mean()\
					.clip(galamsey_aoi)

			# print(sarCollection.size())
			# print(sarCollection.size())
		else:

			sar = sarCollection\
				.filterDate(ee.Date(datefrom), ee.Date(dateto).advance(12, 'day'))\
				.mean()\
				.clip(galamsey_aoi)\

			if coords:
				a = coords.replace("(", "[")
				b = a.replace(")", "]")
				c = b.replace("LatLng", "")

				getbounds = eval('[' + c + ']')

				bound = [swap(aa) for aa in getbounds]

				poly = ee.Geometry.Polygon(bound)

				sar = sarCollection\
					.filterDate(ee.Date(datefrom), ee.Date(dateto).advance(12, 'day'))\
					.mean()\
					.clip(poly)
			else:

				sar = sarCollection\
					.filterDate(ee.Date(datefrom), ee.Date(dateto).advance(12, 'day'))\
					.mean()\
					.clip(galamsey_aoi)\


		Quater = ee.Image.cat([
			sar.select('VV'),
			sar.select('VH').multiply(2).rename('DVH'),
			sar.select('VV').divide(sar.select('VH')).divide(100).rename('PVH')
		])

		threshold = Quater.select(
			'VV').gte(-20) and Quater.select('VV').lte(-10)

		mosdate = datefrom - relativedelta(years=1)

		# //Importing SENTINEL-2 collection

		# print(dateto.date())
		# print(dateto.date().year)
		# print(dateto.date().year)

		if dateto.date().year == 2015 or dateto.date().year == 2016:
			# print("helloo")
			St2 = ee.ImageCollection('COPERNICUS/S2')\
					.filterDate(str(mosdate.date()), "2018-12-31")\
					.filterBounds(galamsey_aoi)\
					.select(['B1', 'B2', 'B3', 'B4', 'B8', 'B9', 'B11', 'B12'])\
				.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5))\
				.median()\
				.clip(galamsey_aoi)
		else:
			# print("helloo2322323")
			St2 = ee.ImageCollection('COPERNICUS/S2')\
					.filterDate(str(mosdate.date()), str(dateto.date()))\
					.filterBounds(galamsey_aoi)\
					.select(['B1', 'B2', 'B3', 'B4', 'B8', 'B9', 'B11', 'B12'])\
				.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5))\
				.median()\
				.clip(galamsey_aoi)

		# // NDVI Composite
		ndvi = St2.normalizedDifference(['B8', 'B4'])

		ndvi1 = ndvi.gt(0.3).Not().selfMask()

		ndvi2 = ndvi.lte(0.018).And(ndvi.gt(-0.07))

		ndviFinal = ndvi2.blend(ndvi1).selfMask()

		# # // Map the ID function over the FeatureCollection and converting to Image (osm settlement).
		osm_settlement = osm_settlement_dataset.map(addIDfunc)\
			.reduceToImage(**{
				'properties': ['id'],
				'reducer': ee.Reducer.first()
			}
		)

		# //Clipping osm_settlement to project area
		mask1 = osm_settlement.clip(galamsey_aoi)

		road_buffer = road_network.map(bufferfunc)

		road = road_buffer.map(addIDfunc)\
			.reduceToImage(**{
				"properties": ['id'],
				"reducer": ee.Reducer.first()
			}
		)

# //Merging or combining all the mask
		mask = mask1.blend(builtup).blend(
			road).mask().clip(galamsey_aoi).selfMask()

# // Creating of final mask
		# maskComposite = ndviFinal.updateMask(mask.Not()).selfMask()
		maskComposite = ndviFinal.updateMask(mask.unmask().Not())


# // Displaying and Visualizing after thresholding
		dataset = threshold.updateMask(
			maskComposite).clip(gala_buffer).selfMask()

		return dataset

	except Exception as e:
		raise e
		return None


# def computeSentinel(start,end,coords=None):
# 	toHTML={}
# 	try:
# 		loaddef()
# 		galamsey_aoi=ee.FeatureCollection("users/mamponsah91/Gala_pilarea")
# 		osm_settlement_dataset=ee.FeatureCollection("users/mamponsah91/osm_settlement")
# 		gala_set=ee.FeatureCollection("users/mamponsah91/gala_set")
# 		consolidated_mask=ee.FeatureCollection("users/mamponsah91/Consolidated_mask")
# 		table=ee.FeatureCollection("users/mamponsah91/gala_road_edit")
# 		gala_buffer=ee.FeatureCollection("users/mamponsah91/Gala_buffer")
# 		road_network=ee.FeatureCollection("users/mamponsah91/Road_network")
# 		builtup=ee.Image("users/mamponsah91/set")


# 		sarCollection = ee.ImageCollection("COPERNICUS/S1_GRD")\
# 		.filterBounds(galamsey_aoi)\
# 		.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))\
# 		.filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))\
# 		.filter(ee.Filter.eq('instrumentMode', 'IW'))\
# 		.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))\


# 		datefrom=datetime.strptime(start,"%Y-%m-%d" )
# 		dateto=datetime.strptime(end,"%Y-%m-%d")


# 		if datefrom == dateto:
# 			sar=sarCollection\
# 			.filterDate(ee.Date(datefrom),ee.Date(dateto).advance(12, 'day'))\
# 			.mean()\
# 			.clip(galamsey_aoi)

# 			# print(sarCollection.size())
# 			# print(sarCollection.size())
# 		else:

# 			sar= sarCollection\
# 			.filterDate(ee.Date(datefrom),ee.Date(dateto).advance(12, 'day'))\
# 			.mean()\
# 			.clip(galamsey_aoi)\


# 		Quater = ee.Image.cat([
# 		sar.select('VV'),
# 		sar.select('VH').multiply(2).rename('DVH'),
# 		sar.select('VV').divide(sar.select('VH')).divide(100).rename('PVH')
# 		]);

# 		threshold = Quater.select('VV').gte(-20) and Quater.select('VV').lte(-10)


# 		# print(threshold)

# 		# //Importing SENTINEL-2 collection


# 		St2 = ee.ImageCollection('COPERNICUS/S2')\
# 			.filterDate('2015-01-01',str(today))\
# 			.filterBounds(galamsey_aoi)\
# 			.select(['B1','B2','B3','B4','B8','B9','B11','B12'])\
# 			  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',5))\
# 			  .median()\
# 			  .clip(galamsey_aoi);


# 		# // NDVI Composite
# 		ndvi = St2.normalizedDifference(['B8','B4']);

# 		ndvi1 = ndvi.gt(0.3).Not().selfMask();

# 		ndvi2 = ndvi.lte(0.018).And(ndvi.gt(-0.07));

# 		ndviFinal = ndvi2.blend(ndvi1).selfMask();


# 		# # // Map the ID function over the FeatureCollection and converting to Image (osm settlement).
# 		osm_settlement = osm_settlement_dataset.map(addIDfunc)\
# 							.reduceToImage(**{
# 							'properties':['id'],
# 							'reducer':ee.Reducer.first()
# 							}
# 							);

# 		# //Clipping osm_settlement to project area
# 		mask1 = osm_settlement.clip(galamsey_aoi)

# 		road_buffer = road_network.map(bufferfunc)

# 		road = road_buffer.map(addIDfunc)\
# 					.reduceToImage(**{
# 					"properties":['id'],
# 					"reducer":ee.Reducer.first()
# 					}
# 					);

# # //Merging or combining all the mask
# 		mask = mask1.blend(builtup).blend(road).mask().clip(galamsey_aoi).selfMask();

# # // Creating of final mask
# 		# maskComposite = ndviFinal.updateMask(mask.Not()).selfMask()
# 		maskComposite = ndviFinal.updateMask(mask.unmask().Not())


# # // Displaying and Visualizing after thresholding
# 		dataset = threshold.updateMask(maskComposite).clip(gala_buffer).selfMask();


# 		if coords:
# 			a = coords.replace("(","[")
# 			b=a.replace(")","]")
# 			c=b.replace("LatLng" ,"")

# 			getbounds=eval('[' + c + ']')

# 			bound = [swap(aa) for aa in getbounds]

# 			poly=ee.Geometry.Polygon(bound)


# 			dataset = dataset.clip(poly);


# 		return dataset

# 	except Exception as e:
# 		raise e
# 		return None


def getchangeDetection(request):
	loaddef()
	toHTML = {}
	start1 = request.GET.get("from")
	end1 = request.GET.get("to")
	start2 = request.GET.get("from1")
	end2 = request.GET.get("to1")

	query1 = computeSentinel(start1, end1)
	query2 = computeSentinel(start2, end2)

	unmask_query1 = query1.unmask()
	unmask_query2 = query2.unmask()
	inactiveQ2Q1_19 = unmask_query2.subtract(unmask_query1).selfMask()

	styling = {'min': 0, 'max': 1, 'palette': ["black"]}
	idfeatures = inactiveQ2Q1_19.getMapId(styling)

	toHTML['mapid'] = str(idfeatures['tile_fetcher'].url_format)
	toHTML['token'] = idfeatures['token']

	return JsonResponse(toHTML, safe=False)


def getchangeDetectionActive(request):
	loaddef()
	toHTML = {}
	start1 = request.GET.get("from")
	end1 = request.GET.get("to")
	start2 = request.GET.get("from1")
	end2 = request.GET.get("to1")

	state = request.GET.get("status")

	query1 = computeSentinel(start1, end1)
	query2 = computeSentinel(start2, end2)

	unmask_query1 = query1.unmask()
	unmask_query2 = query2.unmask()

	if end2 > end1:
		if state == "active":
			processimage = query2.subtract(unmask_query1).selfMask()
		else:
			processimage = query1.subtract(unmask_query2).selfMask()
	else:

		if state == "active":

			processimage = query1.subtract(unmask_query2).selfMask()

		else:
			processimage = query2.subtract(unmask_query1).selfMask()

	if state == "active":
		styling = {'min': 0, 'max': 1, 'palette': ["sandybrown"]}
	else:
		styling = {'min': 0, 'max': 1, 'palette': ["black"]}
	idfeatures = processimage.getMapId(styling)

	toHTML['mapid'] = str(idfeatures['tile_fetcher'].url_format)
	toHTML['token'] = idfeatures['token']

	return JsonResponse(toHTML, safe=False)


def computeArea(dataset, poly=None):
	loaddef()
	if poly:
		galamsey_aoi = poly
	else:
		galamsey_aoi = ee.FeatureCollection("users/mamponsah91/Gala_pilarea")
	dataset = ee.Image(dataset)
	area = dataset.multiply(ee.Image.pixelArea()).divide(1000*1000)

	stat = area.reduceRegion(
		**{
			'reducer': ee.Reducer.sum(),
			'geometry': galamsey_aoi,
			'crs': 'EPSG:4326',
			'scale': 10,
			'maxPixels': 1e13
		})

	# print (stat.getInfo())

	return stat.getInfo()['VV']


def areacomputationChangedetection(request):
	loaddef()
	toHTML = {}
	results = []
	start1 = request.GET.get("from")
	end1 = request.GET.get("to")
	start2 = request.GET.get("from1")
	end2 = request.GET.get("to1")

	coords = request.GET.get("coords")

	if coords:
		a = coords.replace("(", "[")
		b = a.replace(")", "]")
		c = b.replace("LatLng", "")

		getbounds = eval('[' + c + ']')

		bound = [swap(aa) for aa in getbounds]

		poly = ee.Geometry.Polygon(bound)

	query1 = computeSentinel(start1, end1, coords)
	query2 = computeSentinel(start2, end2, coords)

	unmask_query1 = query1.unmask()
	unmask_query2 = query2.unmask()

	if end2 > end1:
		activeQ2Q1_19 = query2.subtract(unmask_query1).selfMask()
		inactive = query1.subtract(unmask_query2).selfMask()
	else:
		activeQ2Q1_19 = query1.subtract(unmask_query2).selfMask()
		inactive = query2.subtract(unmask_query1).selfMask()

	a_quert1 = computeArea(query1, poly)
	a_quert2 = computeArea(query2, poly)
	a_inactive = computeArea(inactive, poly)
	a_activeQ2Q1_19 = computeArea(activeQ2Q1_19, poly)

	results.append(["Query 1",  a_quert1])
	results.append(["Query 2",  a_quert2])
	results.append(["Newly Active",  a_activeQ2Q1_19])
	results.append(["Inactive",  a_inactive])

	# print(a_quert1)
	# print(a_quert2)
	# print(a_inactive)
	# print(a_activeQ2Q1_19)

	toHTML["result"] = results
	# return JsonResponse(toHTML,safe=False)
	return render(request, 'rootApp/changedetchart.html', toHTML)


# def datetime_range(start=None, end=None):
#     span = end - start
#     for i in range(span.days + 1):
#         yield start + timedelta(days=i)

# def year_range(start=None, end=None):
# 	while start <= end:
# 	    int( start ) += 1
# 	    print(start)


def miliconvert(value):
	from datetime import datetime

	dt_obj = datetime.strptime(str(value), '%Y-%m-%d')
	millisec = dt_obj.timestamp() * 1000

	return millisec


def timeseries_view(request):
	loaddef()
	result = []
	datefrom = request.GET.get("tfrom")
	# datetime.strptime(request.GET.get("tfrom"),"%Y-%m-%d" )
	dateto = request.GET.get("tto")

	asd = request.GET.get("coords")
	if asd:
		a = asd.replace("(", "[")
		b = a.replace(")", "]")
		c = b.replace("LatLng", "")
		getbounds = eval('[' + c + ']')
		bound = [swap(aa) for aa in getbounds]
		poly = ee.Geometry.Polygon(bound)

	gop = []
	Q1 = {}
	Q2 = {}
	Q3 = {}
	Q4 = {}

	ranger = range(int(datefrom), int(dateto)+1)
	for aa in ranger:
		Q1 = {"start": 1,
			  "first": 1,
			  "last": 31,
			  "end": 3,
			  "name": "Q1",
			  }
		Q2 = {"start": 4,
			  "first": 1,
			  "last": 30,
			  "name": "Q2",
			  "end": 6
			  }

		Q3 = {"start": 7,
			  "first": 1,
			  "last": 30,
			  "name": "Q3",
			  "end": 9
			  }

		Q4 = {"start": 10,
			  "first": 1,
			  "last": 31,
			  "name": "Q4",
			  "end": 12
			  }
		Q1["year"] = aa
		Q2["year"] = aa
		Q3["year"] = aa
		Q4["year"] = aa
		year = [Q1, Q2, Q3, Q4]

		gop.append(year)

	for aa in gop:
		for bb in aa:

			dfrom = datetime(int(bb["year"]), int(
				bb["start"]), int(bb["first"]))

			dto = datetime(int(bb["year"]), int(bb["end"]), int(bb["last"]))

			dataset = computeSentinel(str(dfrom.date()), str(dto.date()), asd)
			try:
				area = computeArea(dataset, poly)
			except Exception as e:

				area = 0

			result.append([bb["name"]+"_"+str(bb["year"]), area])

	# print(result)

	return render(request, 'rootApp/chart.html', locals())


def datetimeseries_view(request):
	loaddef()
	result = []
	datefrom = datetime.strptime(request.GET.get("tfrom"), "%Y-%m-%d")
	dateto = datetime.strptime(request.GET.get("tto"), "%Y-%m-%d")
	asd = request.GET.get("coords")
	if asd:
		a = asd.replace("(", "[")
		b = a.replace(")", "]")
		c = b.replace("LatLng", "")
		getbounds = eval('[' + c + ']')
		bound = [swap(aa) for aa in getbounds]
		poly = ee.Geometry.Polygon(bound)

	for date in datetime_range(start=datetime(datefrom.year, datefrom.month, datefrom.day), end=datetime(dateto.year, dateto.month, dateto.day)):
		dataset = computeSentinel(str(date.date()), str(date.date()), asd)
		try:
			area = computeArea(dataset, poly)
		except Exception as e:
			area = "null"

		# .strftime('%Y-%m-%d')
		result.append([miliconvert(date.date()), area])
		# asd=date.date()
		# print(date.date())
		# print(area)

	return render(request, 'rootApp/chart2.html', locals())


def maskL8srClouds(image):

	cloudShadowBitMask = (1 << 3)
	cloudsBitMask = (1 << 5)
	qa = image.select('pixel_qa')
	mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)\
		.And(qa.bitwiseAnd(cloudsBitMask).eq(0))
	return image.updateMask(mask)


def loadLandsatComposite(request):
	loaddef()
	toHTML = {}
	galamsey_aoi = ee.FeatureCollection("users/mamponsah91/Gala_pilarea")
	countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
	country = countries.filter(ee.Filter.eq('country_na', 'Ghana'))

	year = request.GET.get("year")

	startDate = str(year)+'-01-01'
	endDate = str(year)+'-12-31'

	l8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')

	l8compositeMasked = l8.filterBounds(country)\
		.filterDate(startDate, endDate)\
		.filterMetadata('CLOUD_COVER', 'less_than', 50)\
		.map(maskL8srClouds)\
		.median()\
		.clip(galamsey_aoi)
	L8_754_viz = {"bands": ['B7', 'B6', 'B4'], "min": [
		500, 500, 500], "max": [2000, 4500, 1500]}

	idfeatures = l8compositeMasked.getMapId(L8_754_viz)

	toHTML['mapid'] = str(idfeatures['tile_fetcher'].url_format)
	toHTML['token'] = idfeatures['token']

	return JsonResponse(toHTML, safe=False)


def loadAoi(request):
	loaddef()
	toHTML = {}
	galamsey_aoi = ee.FeatureCollection("users/mamponsah91/Gala_pilarea")

	style = {'color': 'black', 'fillColor': 'red', 'strokewidth': 7}

	idfeatures = galamsey_aoi.getMapId(style)

	toHTML['mapid'] = str(idfeatures['tile_fetcher'].url_format)
	toHTML['token'] = idfeatures['token']

	return JsonResponse(toHTML, safe=False)
