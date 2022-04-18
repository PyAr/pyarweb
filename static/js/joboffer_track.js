function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function trackContactInfo() {
  const csrftoken = getCookie('csrftoken');

  const targetUrl = `${window.location.href}track-contact-info-view`;

  const request = new Request(
    targetUrl,
    {
      method: 'POST',
      headers: {'X-CSRFToken': csrftoken},
      mode: 'same-origin' // Do not send CSRF token to another domain.
    }
  );
  return fetch(request);
}
