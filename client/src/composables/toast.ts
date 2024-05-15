import { POSITION, useToast } from 'vue-toastification'

/**
 * @description
 * 토스트 알림
 * @param {string} type info, warn, success, error
 * @param {string} text 토스트에 표시할 텍스트
 */
export function showToast(type: string, text: string): void {
  const toast = useToast()
  const options = {
    position: POSITION.TOP_CENTER,
    timeout: 2500
  }
  switch (type) {
    case 'info':
      toast.info(text, options)
      break
    case 'warn':
      toast.warning(text, options)
      break
    case 'success':
      toast.success(text, options)
      break
    case 'error':
      toast.error(text, options)
      break
    default:
      break
  }
}
