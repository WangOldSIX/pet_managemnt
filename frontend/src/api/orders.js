import request from '@/utils/request'

export const getOrderList = (params) => {
  return request({
    url: '/orders',
    method: 'get',
    params
  })
}

export const getOrderDetail = (id) => {
  return request({
    url: `/orders/${id}`,
    method: 'get'
  })
}

export const createOrder = (data) => {
  return request({
    url: '/orders',
    method: 'post',
    data
  })
}

export const updateOrder = (id, data) => {
  return request({
    url: `/orders/${id}`,
    method: 'put',
    data
  })
}

export const deleteOrder = (id) => {
  return request({
    url: `/orders/${id}`,
    method: 'delete'
  })
}
