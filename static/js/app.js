function hablarBienvenida() {
  const mensaje = "Bienvenido a BarneBT-Plus, tu asistente virtual municipal. Puedes decirme qué necesitas y te ayudaré.";
  hablar(mensaje);
}

function hablar(texto) {
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(texto);
  utterance.lang = 'es-AR';
  utterance.rate = 0.95;
  utterance.pitch = 1.1;
  utterance.volume = 1;
  
  utterance.onstart = () => console.log('BarneBT-Plus está hablando...');
  utterance.onend = () => console.log('BarneBT-Plus terminó de hablar');
  
  window.speechSynthesis.speak(utterance);
}

function iniciarReconocimiento() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  
  if (!SpeechRecognition) {
    hablar("Lo siento, tu navegador no soporta reconocimiento de voz.");
    return;
  }
  
  const recognition = new SpeechRecognition();
  recognition.lang = 'es-AR';
  recognition.continuous = false;
  recognition.interimResults = false;
  
  recognition.onstart = () => {
    console.log('Escuchando...');
    hablar("Estoy escuchándote. Cuéntame qué necesitas.");
  };
  
  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript.toLowerCase();
    console.log('Dijiste:', transcript);
    procesarComando(transcript);
  };
  
  recognition.onerror = () => {
    hablar("Disculpa, no pude entender. Intenta de nuevo.");
  };
  
  recognition.start();
}

function procesarComando(transcript) {
  if (transcript.includes('hola') || transcript.includes('buenos')) {
    hablar("¡Hola! Soy BarneBT-Plus, tu asistente virtual.");
  } else if (transcript.includes('trámite') || transcript.includes('solicitud')) {
    hablar("Puedo ayudarte con trámites online. ¿Cuál necesitas?");
  } else if (transcript.includes('whatsapp') || transcript.includes('chat')) {
    hablar("Perfecto, te voy a abrir WhatsApp.");
    setTimeout(() => {
      window.open('https://wa.me/56912345678?text=Hola%20BarneBT-Plus', '_blank');
    }, 1500);
  } else {
    hablar("Entendí: " + transcript + ". ¿Puedes especificar qué servicio necesitas?");
  }
}

document.addEventListener('DOMContentLoaded', function() {
  setTimeout(hablarBienvenida, 800);
  
  if (document.querySelector('h1')) {
    document.querySelector('h1').addEventListener('click', hablarBienvenida);
  }
  
  const micButton = document.createElement('button');
  micButton.innerHTML = ' Habla conmigo';
  micButton.className = 'btn-primary-gradient';
  micButton.style.marginTop = '1rem';
  micButton.onclick = iniciarReconocimiento;
  
  const button = document.querySelector('.btn-primary-gradient');
  if (button) {
    button.parentNode.insertBefore(micButton, button.nextSibling);
  }
});
