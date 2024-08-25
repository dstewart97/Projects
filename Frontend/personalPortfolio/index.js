// --------- FLOATING NAV -----------
const floatingNavs = document.querySelectorAll('.floating_nav a');

const removeActiveCLass = () => {
    floatingNavs.forEach(nav => {
        nav.classList.remove('active')
    });
}

floatingNavs.forEach(nav => {
    nav.addEventListener('click', () => {
        removeActiveCLass();
        nav.classList.add('active')
    })
})




// --------- RESUME -----------
const resumeRight = document.querySelector('.resume_right');
const experienceContent = `<h4>Experience</h4>
                <p>
                    Lorem, ipsum dolor sit amet consectetur adipisicing elit.
                    Earum omnis illo harum aliquid animi facilis quisquam ut
                    facere?
                </p>
                <ul>
                    <li>
                        <h6>2018 - 2019</h6>
                        <h5>Intern</h5>
                        <p>Mobile Telecom Company</p>
                    </li>
                    <li>
                        <h6>2019 - 2021</h6>
                        <h5>Freelance Web Designer</h5>
                        <p>Fiverr and Upwork</p>
                    </li>
                    <li>
                        <h6>2021 - 2022</h6>
                        <h5>Frontend Developer</h5>
                        <p>MTN Ghana</p>
                    </li>
                    <li>
                        <h6>2022 - 2024</h6>
                        <h5>Fullstack Freelancer</h5>
                        <p>Self Employed</p>
                    </li>
                </ul>
`;

const experienceBtn = document.querySelector('.experience_btn');
experienceBtn.addEventListener('click', () => {
    resumeRight.innerHTML = experienceContent;
    resumeRight.className = 'resume_right';
    experienceBtn.classList.add('primary');
    // remove classes from other buttons
    aboutBtn.classList.remove('primary');
    skillsBtn.classList.remove('primary');
    educationBtn.classList.remove('primary');
})
// set experience content as default content for resume_right
resumeRight.innerHTML = experienceContent;

// education
const educationBtn = document.querySelector('.education_btn');
const educationContent = `<h4>Education</h4>
                <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Dolores.</p>
                <ul>
                    <li>
                        <h5>College Education</h5>
                        <p>
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Eligendi voluptas maiores qui doloremque accusantium atque vero facilis.
                        </p>
                    </li>
                    <li>
                        <h5>Frontend Education</h5>
                        <p>
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Eligendi voluptas maiores qui doloremque accusantium atque vero facilis.
                        </p>
                    </li>
                    <li>
                        <h5>Backend Education</h5>
                        <p>
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Eligendi voluptas maiores qui doloremque accusantium atque vero facilis.
                        </p>
                    </li>
                </ul>
`;

educationBtn.addEventListener('click', () => {
    resumeRight.innerHTML = educationContent;
    resumeRight.className = 'resume_right education';
    educationBtn.classList.add('primary');
    //remove classes from other buttons
    aboutBtn.classList.remove('primary');
    skillsBtn.classList.remove('primary');
    experienceBtn.classList.remove('primary');
})


// skills
const skillsBtn = document.querySelector('.skills_btn');
const skillsContent = `<h4>Skills</h4>
<p>Lorem ipsum dolor sit amet consectetur.</p>
<ul>
    <li><img src="./media/react.webp" alt="ReactJS logo"></li>
    <li><img src="./media/next.png" alt="NextJS logo"></li>
    <li><img src="./media/tailwind.png" alt="Tailwind logo"></li>
    <li><img src="./media/prisma.png" alt="Prisma logo"></li>
    <li><img src="./media/mongo.jpg" alt="MongoDB logo"></li>
    <li><img src="./media/jwt.png" alt="JWT logo"></li>
    <li><img src="./media/node.png" alt="NodeJS logo"></li>
</ul>
`;

skillsBtn.addEventListener('click', () => {
    resumeRight.innerHTML = skillsContent;
    resumeRight.className = 'resume_right skills';
    skillsBtn.classList.add('primary');
    //remove classes from other buttons
    aboutBtn.classList.remove('primary');
    educationBtn.classList.remove('primary');
    experienceBtn.classList.remove('primary');
})


// about me
const aboutBtn = document.querySelector('.about_btn');
aboutContent = `<h4>About me</h4>
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Velit debitis excepturi quibusdam.</p>
                <ul>
                    <li>
                        <h6>Name:</h6>
                        <h5>Ernest Achiever</h5>
                    </li>
                    <li>
                        <h6>Experience:</h6>
                        <h5>6+ years</h5>
                    </li>
                    <li>
                        <h6>Email:</h6>
                        <h5>youremail@gmail.com</h5>
                    </li>
                    <li>
                        <h6>Nationality:</h6>
                        <h5>Ghanaian</h5>
                    </li>
                    <li>
                        <h6>Freelance & collabs:</h6>
                        <h5>Available</h5>
                    </li>
                    <li>
                        <h6>Language:</h6>
                        <h5>English</h5>
                    </li>
                    <li>
                        <h6>Phone:</h6>
                        <h5>+233557097546</h5>
                    </li>
                    <li>
                        <h6>LinkedIn:</h6>
                        <h5>@yourhandle</h5>
                    </li>
                </ul>
`;

aboutBtn.addEventListener('click', () => {
    resumeRight.innerHTML = aboutContent;
    resumeRight.className = 'resume_right about';
    aboutBtn.classList.add('primary');
    //remove classes from other buttons
    skillsBtn.classList.remove('primary');
    educationBtn.classList.remove('primary');
    experienceBtn.classList.remove('primary');
})



// --------- MIXITUP PROJECTS SECTION -----------
const containerEl = document.querySelector('.projects_container');
let mixer = mixitup(containerEl, {
    animation: {
        enable: false
    }
})

mixer.filter('*')



// --------- SWIPER -----------
const swiper = new Swiper('.swiper', {
    // Optional parameters
    loop: true,
    slidesPerView: 1,
    spacebetween: 30,

    // If we need pagination
    pagination: {
        el: '.swiper-pagination',
        clickable: true
    },
    breakpoints: {
        600: {
            slidesPerView: 2
        },
        1024: {
            slidesPerView: 3
        }
    }

});


// --------- FAQs -----------
const faqs = document.querySelectorAll('.faqs_item');

faqs.forEach(faq => {
    faq.addEventListener('click', () => {
        const p = faq.querySelector('p');
        const icon = faq.querySelector('.faq_icon');
        if (p.classList.contains('show')) {
            p.classList.remove('show')
            icon.innerHTML = `<i class="uil uil-angle-down"></i>`
        } else {
            p.classList.add('show')
            icon.innerHTML = `<i class="uil uil-angle-up"></i>`
        }
    })
})


// --------- DARK THEME -----------
const themeToggler = document.querySelector('.nav_theme-btn');
themeToggler.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme-variables')
    if(document.body.className == '') {
        themeToggler.innerHTML = `<i class="uil uil-moon"></i>`
        window.localStorage.setItem('portfolio-theme', '')
    } else {
        themeToggler.innerHTML = `<i class="uil uil-sun"></i>`
        window.localStorage.setItem('portfolio-theme', 'dark-theme-variables')
    }
})

// set theme from local storage on page load
const bodyClass = window.localStorage.getItem('portfolio-theme');
document.body.className = bodyClass;