import request from '@/utils/request'

export const getServiceList = (params) => {
  return request({
    url: '/services',
    method: 'get',
    params
  })
}

export const getServiceDetail = (id) => {
  return request({
    url: `/services/${id}`,
    method: 'get'
  })
}

export const createService = (data) => {
  return request({
    url: '/services',
    method: 'post',
    data
  })
}

export const updateService = (id, data) => {
  return request({
    url: `/services/${id}`,
    method: 'put',
    data
  })
}

export const deleteService = (id) => {
  return request({
    url: `/services/${id}`,
    method: 'delete'
  })
}
