from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage



def page_list(request,obj):
  query_page = request.POST['page'] if request.POST['page'] else 1
  rows = request.POST['rows'] if request.POST['rows'] else 1
  list = Paginator(obj,rows)
  last_page = list.num_pages
  records = list.count
  try:
        info = list.page(query_page)
        return {'page':str(query_page),'last':last_page,'data':info,'records':records}
  except PageNotAnInteger:
        info = list.page(1)
        return {'page': '1', 'last': last_page, 'data': info,'records':records}
  except EmptyPage :
         info = list.page(last_page)
         return {'page': str(last_page), 'last': last_page, 'data': info,'records':records}

      
  

