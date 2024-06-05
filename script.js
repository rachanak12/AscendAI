const signUpButton=document.getElementById('signUpButton');
const signInButton=document.getElementById('signInButton');
const signInForm=document.getElementById('signIn');
const signUpForm=document.getElementById('signup');

signUpButton.addEventListener('click',function(){
    signInForm.style.display="none";
    signUpForm.style.display="block";
})
signInButton.addEventListener('click', function(){
    signInForm.style.display="block";
    signUpForm.style.display="none";
})
document.addEventListener("DOMContentLoaded", function() {
  const signInButton = document.getElementById("submitSignIn");

  signInButton.addEventListener("click", function(event) {
    event.preventDefault(); // Prevent the default form submission behavior
    window.location.href = "landing-page-02.html";
  });
});
  