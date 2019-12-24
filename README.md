<html>
<body>
<!--Sport analysis HardTech Enterpreneurship backend infrastructure-->
<h1 class="title">JSON web token authetication and authorization</h1>
<h3 class="why">Why</h3>
<p class="why">This project was created for Data Security subject at Technical University of Denmark during my MSc of Computer Science and Engineering studies.</p>
<h3 class="what">What</h3>
<p class="what">The goal of the project was to create a simple printer interface whose methods can be invoked remotely. Such an interface should be properly secured in order to prevent unauthenticated users from invoking the printer's method. Moreover, different users have different user's permissions, so authorization mechanism is also needed.</p>
<h3 class="how">How</h3>
<p class="how">Both authentication and authorization mechanisms were implemented using JSON Web Token authentication. In order to invoke methods, user needs to provide a JWT token. In order to obtain one, the user needs to log in. User's credentials are stored on the server in a file, where passwords are hashed using a salt. On every method invocation, the user must provide his token, which is verified by the server for validity. The policy file on the server stores information regarding what actions a specific user is allowed to perform against the server.</p>
<h3 class="technologies">Technologies used</h3>
<ul class="technologies">
  <li class="technologies">Java</li>
  <li class="technologies" hover="JSON Web Token">JWT</li>
  <li class="technologies" hover="Remote Method Invocation">RMI</li>
</ul>
<h3 class="usage">How to use</h3>
<p class="usage">In progress.</p>
<hr>
<small class="created">Created: November 2018</small>
</body>
</html>
