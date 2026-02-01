import request from '@/utils/request'

export const getPetList = (params) => {
  return request({
    url: '/pets',
    method: 'get',
    params
  })
}

export const getPetDetail = (id) => {
  return request({
    url: `/pets/${id}`,
    method: 'get'
  })
}

export const createPet = (data) => {
  return request({
    url: '/pets',
    method: 'post',
    data
  })
}

export const updatePet = (id, data) => {
  return request({
    url: `/pets/${id}`,
    method: 'put',
    data
  })
}

export const deletePet = (id) => {
  return request({
    url: `/pets/${id}`,
    method: 'delete'
  })
}
