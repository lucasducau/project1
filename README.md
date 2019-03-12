<html><head>

      

        <title>Project 1: Books</title>

    </head>

    <body>
        <div class="container-lg px-3 my-3 markdown-body">
            <h1 id="project-1-books">Project 1: Books</h1>

<h2 id="objectives">Objectives</h2>

<ul>
  <li>Become more comfortable with Python.</li>
  <li>Gain experience with Flask.</li>
  <li>Learn to use SQL to interact with databases.</li>
</ul>

<h2 id="overview">Overview</h2>

<p>In this project, you’ll build a book review website. Users will be able to
register for your website and then log in using their username and password.
Once they log in, they will be able to search for books, leave reviews for
individual books, and see the reviews made by other people.
You’ll also use the a third-party API by Goodreads, another book review website,
to pull in ratings from a broader audience.
Finally, users will be able to query for book details and book reviews
programmatically via your website’s API.</p>

<h2 id="getting-started">Getting Started</h2>

<h3 id="postgresql">PostgreSQL</h3>

<p>For this project, you’ll need to set up a PostgreSQL database to use with our
application. It’s possible to set up PostgreSQL locally on your own computer,
but for this project, we’ll use a database hosted by
<a href="https://www.heroku.com/">Heroku</a>, an online web hosting service.</p>

<ol>
  <li>Navigate to <a href="https://www.heroku.com/">https://www.heroku.com/</a>, and create
an account if you don’t already have one.</li>
  <li>On Heroku’s Dashboard, click “New” and choose “Create new app.”</li>
  <li>Give your app a name, and click “Create app.”</li>
  <li>On your app’s “Overview” page, click the “Configure Add-ons” button.</li>
  <li>In the “Add-ons” section of the page, type in and select “Heroku Postgres.”</li>
  <li>Choose the “Hobby Dev - Free” plan, which will give you access to a free
PostgreSQL database that will support up to 10,000 rows of data. Click
“Provision.”</li>
  <li>Now, click the “Heroku Postgres :: Database” link.</li>
  <li>You should now be on your database’s overview page. Click on “Settings”, and
then “View Credentials.” This is the information you’ll need to log into your
database. You can access the database via
<a href="https://adminer.cs50.net/">Adminer</a>, filling in the server (the “Host” in
the credentials list), your username (the “User”), your password, and the
name of the database, all of which you can find on the Heroku credentials
page.</li>
</ol>

<p>Alternatively, if you install
<a href="https://www.postgresql.org/download/">PostgreSQL</a> on your own computer, you
should be able to run <code class="highlighter-rouge">psql URI</code> on the command line, where the <code class="highlighter-rouge">URI</code> is
the link provided in the Heroku credentials list.</p>

<h3 id="python-and-flask">Python and Flask</h3>

<ol>
  <li>First, make sure you install a copy of
  <a href="https://www.python.org/downloads/">Python</a>. For this course, you should be using
  Python version 3.6 or higher.</li>
  <li>You’ll also need to install <code class="highlighter-rouge">pip</code>. If you downloaded Python from Python’s
  website, you likely already have <code class="highlighter-rouge">pip</code> installed (you can check by running
  <code class="highlighter-rouge">pip</code> in a terminal window). If you don’t have it installed, be sure to
  <a href="https://pip.pypa.io/en/stable/installing/">install it</a> before moving on!</li>
</ol>

<p>To try running your first Flask
application:</p>

<ol>
  <li>Download the <code class="highlighter-rouge">project1</code> distribution directory from https://cdn.cs50.net/web/2018/spring/projects/1/project1.zip and unzip it.</li>
  <li>In a terminal window, navigate into your <code class="highlighter-rouge">project1</code> directory.</li>
  <li>Run <code class="highlighter-rouge">pip3 install -r requirements.txt</code> in your terminal window to make sure
that all of the necessary Python packages (Flask and SQLAlchemy, for
instance) are installed.</li>
  <li>Set the environment variable <code class="highlighter-rouge">FLASK_APP</code> to be <code class="highlighter-rouge">application.py</code>. On a Mac or
on Linux, the command to do this is <code class="highlighter-rouge">export FLASK_APP=application.py</code>. On
Windows, the command is instead <code class="highlighter-rouge">set FLASK_APP=application.py</code>. You may
optionally want to set the environment variable <code class="highlighter-rouge">FLASK_DEBUG</code> to <code class="highlighter-rouge">1</code>, which
will activate Flask’s debugger and will automatically reload your web
application whenever you save a change to a file.</li>
  <li>Set the environment variable <code class="highlighter-rouge">DATABASE_URL</code> to be the URI of your database,
which you should be able to see from the credentials page on Heroku.</li>
  <li>Run <code class="highlighter-rouge">flask run</code> to start up your Flask application.</li>
  <li>If you navigate to the URL provided by <code class="highlighter-rouge">flask</code>, you should see the text
<code class="highlighter-rouge">"Project 1: TODO"</code>!</li>
</ol>

<h3 id="goodreads-api">Goodreads API</h3>

<p>Goodreads is a popular book review website, and we’ll be using their API in this
project to get access to their review data for individual books.</p>

<ol>
  <li>Go to <a href="https://www.goodreads.com/api">https://www.goodreads.com/api</a> and sign
up for a Goodreads account if you don’t already have one.</li>
  <li>Navigate to
<a href="https://www.goodreads.com/api/keys">https://www.goodreads.com/api/keys</a> and
apply for an API key. For “Application name” and “Company name” feel free to
just write “project1,” and no need to incluce an application URL, callback
URL, or support URL.</li>
  <li>You should then see your API key. (For this project, we’ll care only about the
“key”, not the “secret”.)</li>
  <li>You can now use that API key to make requests to the Goodreads API,
documented <a href="https://www.goodreads.com/api/index">here</a>. In particular, Python
code like the below</li>
</ol>

<div class="language-py highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kn">import</span> <span class="nn">requests</span>
<span class="n">res</span> <span class="o">=</span> <span class="n">requests</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">"https://www.goodreads.com/book/review_counts.json"</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="p">{</span><span class="s">"key"</span><span class="p">:</span> <span class="s">"KEY"</span><span class="p">,</span> <span class="s">"isbns"</span><span class="p">:</span> <span class="s">"9781632168146"</span><span class="p">})</span>
<span class="k">print</span><span class="p">(</span><span class="n">res</span><span class="o">.</span><span class="n">json</span><span class="p">())</span>
</code></pre></div></div>

<p>where <code class="highlighter-rouge">KEY</code> is your API key, will give you the review and rating data for the
book with the provided ISBN number. In particular, you might see something like
this dictionary:</p>

<div class="language-py highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">{</span><span class="s">'books'</span><span class="p">:</span> <span class="p">[{</span>
                <span class="s">'id'</span><span class="p">:</span> <span class="mi">29207858</span><span class="p">,</span>
                <span class="s">'isbn'</span><span class="p">:</span> <span class="s">'1632168146'</span><span class="p">,</span>
                <span class="s">'isbn13'</span><span class="p">:</span> <span class="s">'9781632168146'</span><span class="p">,</span>
                <span class="s">'ratings_count'</span><span class="p">:</span> <span class="mi">0</span><span class="p">,</span>
                <span class="s">'reviews_count'</span><span class="p">:</span> <span class="mi">1</span><span class="p">,</span>
                <span class="s">'text_reviews_count'</span><span class="p">:</span> <span class="mi">0</span><span class="p">,</span>
                <span class="s">'work_ratings_count'</span><span class="p">:</span> <span class="mi">26</span><span class="p">,</span>
                <span class="s">'work_reviews_count'</span><span class="p">:</span> <span class="mi">113</span><span class="p">,</span>
                <span class="s">'work_text_reviews_count'</span><span class="p">:</span> <span class="mi">10</span><span class="p">,</span>
                <span class="s">'average_rating'</span><span class="p">:</span> <span class="s">'4.04'</span>
            <span class="p">}]</span>
<span class="p">}</span>
</code></pre></div></div>

<p>Note that <code class="highlighter-rouge">work_ratings_count</code> here is the number of ratings that this
particular book has received, and <code class="highlighter-rouge">average_rating</code> is the book’s average score
out of 5.</p>

<h2 id="requirements">Requirements</h2>

<p>Alright, it’s time to actually build your web application! Here are the
requirements:</p>

<ul>
  <li><strong>Registration</strong>: Users should be able to register for your website, providing
(at minimum) a username and password.</li>
  <li><strong>Login</strong>: Users, once registered, should be able to log in to your website
with their username and password.</li>
  <li><strong>Logout</strong>: Logged in users should be able to log out of the site.</li>
  <li><strong>Import</strong>: Provided for you in this project is a file called <code class="highlighter-rouge">books.csv</code>,
which is a spreadsheet in CSV format of 5000 different books.
Each one has an ISBN number, a title, an author, and a publication year.
In a Python file called <code class="highlighter-rouge">import.py</code> separate from your web application,
write a program that will
take the books and import them into your PostgreSQL database. You will first need to
decide what table(s) to create, what columns those tables should have, and how
they should relate to one another. Run this program by running
<code class="highlighter-rouge">python3 import.py</code> to import the books into
your database, and submit this program with the rest of your project code.</li>
  <li><strong>Search</strong>: Once a user has logged in, they should be taken to a page where
they can search for a book. Users should be able to type in the ISBN number of
a book, the title of a book, or the author of a book. After performing the
search, your website should display a list of possible matching results, or
some sort of message if there were no matches. If the user typed in only part
of a title, ISBN, or author name, your search page should find matches for
those as well!</li>
  <li><strong>Book Page</strong>: When users click on a book from the results of the search page,
they should be taken to a book page, with details about the book: its title,
author, publication year, ISBN number, and any reviews that users have left
for the book on your website.</li>
  <li><strong>Review Submission</strong>: On the book page, users should be able to submit a
review: consisting of a rating on a scale of 1 to 5, as well as a text
component to the review where the user can write their opinion about a book.
Users should not be able to submit multiple reviews for the same book.</li>
  <li><strong>Goodreads Review Data</strong>: On your book page, you should also display (if
available) the average rating and number of ratings the work has received from
Goodreads.</li>
  <li><strong>API Access</strong>: If users make a GET request to your website’s <code class="highlighter-rouge">/api/&lt;isbn&gt;</code>
route, where <code class="highlighter-rouge">&lt;isbn&gt;</code> is an ISBN number, your website should return a JSON
response containing the book’s title, author, publication date, ISBN number,
review count, and average score. The resulting JSON should follow the format:</li>
</ul>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">{</span>
    <span class="s">"title"</span><span class="p">:</span> <span class="s">"Memory"</span><span class="p">,</span>
    <span class="s">"author"</span><span class="p">:</span> <span class="s">"Doug Lloyd"</span><span class="p">,</span>
    <span class="s">"year"</span><span class="p">:</span> <span class="mi">2015</span><span class="p">,</span>
    <span class="s">"isbn"</span><span class="p">:</span> <span class="s">"1632168146"</span><span class="p">,</span>
    <span class="s">"review_count"</span><span class="p">:</span> <span class="mi">28</span><span class="p">,</span>
    <span class="s">"average_score"</span><span class="p">:</span> <span class="mf">5.0</span>
<span class="p">}</span>
</code></pre></div></div>

<p>If the requested ISBN number isn’t in your
  database, your website should return a 404 error.</p>
<ul>
  <li>You should be using raw SQL commands (as via SQLAlchemy’s <code class="highlighter-rouge">execute</code> method) in
order to make database queries. You should not use the SQLAlchemy ORM (if
familiar with it) for this project.</li>
  <li>In <code class="highlighter-rouge">README.md</code>, include a short writeup describing your project, what’s
contained in each file, and (optionally) any other additional information the
staff should know about your project.</li>
  <li>If you’ve added any Python packages that need to be installed in order to run
your web application, be sure to add them to <code class="highlighter-rouge">requirements.txt</code>!</li>
</ul>

<p>Beyond these requirements, the design, look, and feel of the website are up to
you! You’re also welcome to add additional features to your website, so long as
you meet the requirements laid out in the above specification!</p>

<h2 id="hints">Hints</h2>

<ul>
  <li>At minimum, you’ll probably want at least one table to keep track of users,
one table to keep track of books, and one table to keep track of reviews. But
you’re not limited to just these tables, if you think others would be helpful!</li>
  <li>In terms of how to “log a user in,” recall that you can store information
inside of the <code class="highlighter-rouge">session</code>, which can store different values for different users.
In particular, if each user has an <code class="highlighter-rouge">id</code>, then you could store that <code class="highlighter-rouge">id</code> in the
session (e.g., in <code class="highlighter-rouge">session["user_id"]</code>) to keep track of which user is
currently logged in.</li>
</ul>

<h2 id="faqs">FAQs</h2>

<h3 id="for-the-api-do-the-json-keys-need-to-be-in-order">For the API, do the JSON keys need to be in order?</h3>

<p>Any order is fine!</p>

<h3 id="attributeerror-nonetype-object-has-no-attribute-_instantiate_plugins"><code class="highlighter-rouge">AttributeError: 'NoneType' object has no attribute '_instantiate_plugins'</code></h3>

<p>Make sure that you’ve set your <code class="highlighter-rouge">DATABASE_URL</code> environment variable before running
<code class="highlighter-rouge">flask run</code>!</p>

<h2 id="how-to-submit">How to Submit</h2>

<ol>
  <li>
    <p>Using <a href="https://git-scm.com/downloads">Git</a>, push your work to <code class="highlighter-rouge">https://github.com/submit50/USERNAME.git</code>, where <code class="highlighter-rouge">USERNAME</code> is your GitHub username, on a branch called <code class="highlighter-rouge">cs50/web/2018/x/projects/1</code> or, if you’ve installed <a href="https://cs50.readthedocs.io/submit50/"><code class="highlighter-rouge">submit50</code></a>, execute</p>

    <div class="highlighter-rouge"><div class="highlight"><pre class="highlight"><code>submit50 cs50/web/2018/x/projects/1
</code></pre></div>    </div>

    <p>instead.</p>
  </li>
  <li><a href="https://www.howtogeek.com/205742/how-to-record-your-windows-mac-linux-android-or-ios-screen/">Record a 1- to 5-minute screencast</a> in which you demonstrate your app’s functionality and/or walk viewers through your code. <a href="https://www.youtube.com/upload">Upload that video to YouTube</a> (as unlisted or public, but not private) or somewhere else.</li>
  <li><a href="https://forms.cs50.io/35643afd-5a3b-4482-bcec-ddbc61af297f">Submit this form</a>.</li>
</ol>

        </div>
    


</body></html>
