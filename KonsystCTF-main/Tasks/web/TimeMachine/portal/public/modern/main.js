document.addEventListener('DOMContentLoaded', () => {
  // Фикс 2
  const sendData = async () => {
      try {
          await fetch('/api/screen', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              credentials: 'include',
              body: JSON.stringify({
                  width: screen.width,
                  height: screen.height
              })
          });

          // Отправляем дату
          await fetch('/api/date', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              credentials: 'include',
              body: JSON.stringify({
                  date: new Date().toISOString()
              })
          });
      } catch(e) {
          console.error('Ошибка отправки данных:', e);
      }
  };
  
  sendData();
});