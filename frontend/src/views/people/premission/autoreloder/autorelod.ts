import { ElMessageBox } from 'element-plus'

export function showSuccessAndReload(message: string, delay: number = 3000) {
  const autoReload = new Promise<void>((resolve) => {
    setTimeout(() => {
      resolve();
    }, delay);
  });

  const clickOk = ElMessageBox.alert(`${message} The page will reload in ${delay / 1000} seconds.`, 'Success');

  Promise.race([clickOk, autoReload]).then(() => {
    window.location.reload();
  });
}