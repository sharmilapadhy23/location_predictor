document.addEventListener('DOMContentLoaded', () => {
    const signInForm = document.querySelector('.sign-in');
    const signUpForm = document.querySelector('.sign-up');
  
    const showSignUp = document.getElementById('showSignUp');
    const showSignIn = document.getElementById('showSignIn');
  
    showSignUp.addEventListener('click', () => {
      gsap.to(signInForm, { x: '-100%', opacity: 0, duration: 0.5 });
      gsap.to(signUpForm, { x: '0%', opacity: 1, duration: 0.5, delay: 0.3 });
      signInForm.classList.add('hidden');
      signUpForm.classList.remove('hidden');
    });
  
    showSignIn.addEventListener('click', () => {
      gsap.to(signUpForm, { x: '100%', opacity: 0, duration: 0.5 });
      gsap.to(signInForm, { x: '0%', opacity: 1, duration: 0.5, delay: 0.3 });
      signUpForm.classList.add('hidden');
      signInForm.classList.remove('hidden');
    });
  });
  document.getElementById("signInForm").addEventListener("submit", function(e) {
    e.preventDefault();  // Prevent default form submission
    // Redirect to the dashboard after sign in
    window.location.href = "../dashboard/dashboard.html";
  });
  
  document.getElementById("signUpForm").addEventListener("submit", function(e) {
    e.preventDefault();  // Prevent default form submission
    // Redirect to the dashboard after sign up
    window.location.href = "../dashboard/dashboard.html";
  });
  