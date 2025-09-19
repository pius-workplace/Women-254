(function() {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  mobileNavToggleBtn.addEventListener('click', mobileNavToogle);

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Chat widget
   */
  let chatWidget = document.querySelector('.chat-widget');

  function toggleChatWidget() {
    if (chatWidget) {
      window.scrollY > 100 ? chatWidget.classList.add('active') : chatWidget.classList.remove('active');
    }
  }

  window.addEventListener('load', toggleChatWidget);
  document.addEventListener('scroll', toggleChatWidget);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Frequently Asked Questions Toggle
   */
  document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle').forEach((faqItem) => {
    faqItem.addEventListener('click', () => {
      faqItem.parentNode.classList.toggle('faq-active');
    });
  });

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /**
   * Correct scrolling position upon page load for URLs containing hash links.
   */
  window.addEventListener('load', function(e) {
    if (window.location.hash) {
      if (document.querySelector(window.location.hash)) {
        setTimeout(() => {
          let section = document.querySelector(window.location.hash);
          let scrollMarginTop = getComputedStyle(section).scrollMarginTop;
          window.scrollTo({
            top: section.offsetTop - parseInt(scrollMarginTop),
            behavior: 'smooth'
          });
        }, 100);
      }
    }
  });

  /**
   * Navmenu Scrollspy
   */
  let navmenulinks = document.querySelectorAll('.navmenu a');

  function navmenuScrollspy() {
    navmenulinks.forEach(navmenulink => {
      if (!navmenulink.hash) return;
      let section = document.querySelector(navmenulink.hash);
      if (!section) return;
      let position = window.scrollY + 200;
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        document.querySelectorAll('.navmenu a.active').forEach(link => link.classList.remove('active'));
        navmenulink.classList.add('active');
      } else {
        navmenulink.classList.remove('active');
      }
    })
  }
  window.addEventListener('load', navmenuScrollspy);
  document.addEventListener('scroll', navmenuScrollspy);

  /**
   * Language toggle functionality
   */
  const languageLinks = document.querySelectorAll('#navmenu [data-lang]');
  const textElements = {
    en: {
      home: "Home",
      about: "About",
      services: "Services",
      counseling: "Counseling",
      legalAid: "Legal Aid",
      emergencySupport: "Emergency Support",
      emergency: "Emergency",
      chat: "Chat",
      language: "Language",
      contact: "Contact",
      emergencyHelp: "Emergency Help",
      welcomeTitle: "Welcome to She Bot",
      welcomeText: "Your safe space for support and empowerment in Kenya. Access help for gender-based violence and mental health.",
      whoWeAreTitle: "Empowering Women in Kenya Through Safe Support",
      whoWeAreText: "She Bot is dedicated to providing trauma-informed support for women facing gender-based violence and mental health challenges in Kenya. We offer confidential counseling, legal assistance, and immediate emergency help.",
      whoWeAreList1: "Confidential and safe counseling services.",
      whoWeAreList2: "Legal aid for survivors of GBV.",
      whoWeAreList3: "24/7 access to emergency helplines and resources.",
      immediateSupportTitle: "Immediate Support",
      immediateSupportDesc: "Quick access to emergency helplines and crisis intervention for gender-based violence.",
      counselingServicesTitle: "Counseling Services",
      counselingServicesDesc: "Confidential mental health support and trauma-informed counseling for women in Kenya.",
      legalAssistanceTitle: "Legal Assistance",
      legalAssistanceDesc: "Access to legal aid, protection orders, and support for survivors of GBV.",
      emergencyHelplinesTitle: "Emergency Helplines",
      emergencyHelplinesDesc: "Immediate support for gender-based violence and mental health crises in Kenya.",
      genderViolenceRecoveryFund: "Gender Violence Recovery Fund",
      genderViolenceRecoveryFundCall: "Call: 1199 (Toll-free)",
      genderViolenceRecoveryFundDesc: "Support for survivors of gender-based violence across Kenya.",
      befriendersKenya: "Befrienders Kenya",
      befriendersKenyaCall: "Call: +254 722 178 177",
      befriendersKenyaDesc: "24/7 emotional support for mental health crises."
    },
    sw: {
      home: "Nyumbani",
      about: "Kuhusu",
      services: "Huduma",
      counseling: "Ushauri",
      legalAid: "Msaada wa Kisheria",
      emergencySupport: "Msaada wa Dharura",
      emergency: "Dharura",
      chat: "Mazungumzo",
      language: "Lugha",
      contact: "Mawasiliano",
      emergencyHelp: "Msaada wa Dharura",
      welcomeTitle: "Karibu She Bot",
      welcomeText: "Mahali pako salama pa kupata msaada na nguvu nchini Kenya. Pata msaada kwa ukatili wa kijinsia na afya ya akili.",
      whoWeAreTitle: "Kuwawezesha Wanawake Kenya Kupitia Msaada Salama",
      whoWeAreText: "She Bot inajitolea kutoa msaada unaozingatia majeraha kwa wanawake wanaokumbwa na ukatili wa kijinsia na changamoto za afya ya akili nchini Kenya. Tunatoa ushauri wa siri, msaada wa kisheria, na msaada wa dharura mara moja.",
      whoWeAreList1: "Huduma za ushauri wa siri na salama.",
      whoWeAreList2: "Msaada wa kisheria kwa waathirika wa ukatili wa kijinsia.",
      whoWeAreList3: "Upatikanaji wa huduma za dharura saa 24/7 na rasilimali.",
      immediateSupportTitle: "Msaada wa Mara Moja",
      immediateSupportDesc: "Upatikanaji wa haraka wa nambari za msaada wa dharura na uingiliaji wa dharura kwa ukatili wa kijinsia.",
      counselingServicesTitle: "Huduma za Ushauri",
      counselingServicesDesc: "Msaada wa afya ya akili wa siri na ushauri unaozingatia majeraha kwa wanawake nchini Kenya.",
      legalAssistanceTitle: "Msaada wa Kisheria",
      legalAssistanceDesc: "Upatikanaji wa msaada wa kisheria, amri za ulinzi, na msaada kwa waathirika wa ukatili wa kijinsia.",
      emergencyHelplinesTitle: "Nambari za Msaada wa Dharura",
      emergencyHelplinesDesc: "Msaada wa haraka kwa ukatili wa kijinsia na changamoto za afya ya akili nchini Kenya.",
      genderViolenceRecoveryFund: "Mfuko wa Urejeshaji wa Ukatili wa Kijinsia",
      genderViolenceRecoveryFundCall: "Piga: 1199 (Bila malipo)",
      genderViolenceRecoveryFundDesc: "Msaada kwa waathirika wa ukatili wa kijinsia kote Kenya.",
      befriendersKenya: "Befrienders Kenya",
      befriendersKenyaCall: "Piga: +254 722 178 177",
      befriendersKenyaDesc: "Msaada wa hisia saa 24/7 kwa changamoto za afya ya akili."
    }
  };

  function setLanguage(lang) {
    if (!textElements[lang]) return;
    document.querySelector('#navmenu a[href$="#hero"]').textContent = textElements[lang].home;
    document.querySelector('#navmenu a[href$="#about"]').textContent = textElements[lang].about;
    const servicesDropdown = document.querySelector('#navmenu li.dropdown > a > span');
    if (servicesDropdown) servicesDropdown.textContent = textElements[lang].services;
    const servicesLinks = document.querySelectorAll('#navmenu li.dropdown ul li a');
    if (servicesLinks.length >= 3) {
      servicesLinks[0].textContent = textElements[lang].counseling;
      servicesLinks[1].textContent = textElements[lang].legalAid;
      servicesLinks[2].textContent = textElements[lang].emergencySupport;
    }
    const emergencyLink = document.querySelector('#navmenu a[href$="#emergency"]');
    if (emergencyLink) emergencyLink.textContent = textElements[lang].emergency;
    const chatLink = document.querySelector('#navmenu a[href="#chat"]');
    if (chatLink) chatLink.textContent = textElements[lang].chat;
    const languageDropdown = document.querySelector('#navmenu li.dropdown:last-child > a > span');
    if (languageDropdown) languageDropdown.textContent = textElements[lang].language;
    document.querySelector('#navmenu a.btn-emergency').textContent = textElements[lang].emergencyHelp;

    // Hero section
    const heroTitle = document.querySelector('#hero h1 span');
    if (heroTitle) heroTitle.textContent = textElements[lang].welcomeTitle.replace("She Bot", "");
    const heroParagraph = document.querySelector('#hero p[data-aos-delay="100"]');
    if (heroParagraph) heroParagraph.textContent = textElements[lang].welcomeText;

    // About section
    const aboutTitle = document.querySelector('.about .who-we-are');
    if (aboutTitle) aboutTitle.textContent = textElements[lang].whoWeAreTitle;
    const aboutText = document.querySelector('.about .fst-italic');
    if (aboutText) aboutText.textContent = textElements[lang].whoWeAreText;
    const aboutListItems = document.querySelectorAll('.about ul li span');
    if (aboutListItems.length >= 3) {
      aboutListItems[0].textContent = textElements[lang].whoWeAreList1;
      aboutListItems[1].textContent = textElements[lang].whoWeAreList2;
      aboutListItems[2].textContent = textElements[lang].whoWeAreList3;
    }
    const aboutReadMore = document.querySelector('.about .read-more span');
    if (aboutReadMore) aboutReadMore.textContent = textElements[lang].whoWeAreTitle.includes("Kuwawezesha") ? "Jifunze Zaidi" : "Learn More";

    // Featured Services section
    const featuredServicesTitles = document.querySelectorAll('#featured-services .service-item h4.title a');
    const featuredServicesDescriptions = document.querySelectorAll('#featured-services .service-item p.description');
    if (featuredServicesTitles.length >= 3 && featuredServicesDescriptions.length >= 3) {
      featuredServicesTitles[0].textContent = textElements[lang].immediateSupportTitle;
      featuredServicesDescriptions[0].textContent = textElements[lang].immediateSupportDesc;
      featuredServicesTitles[1].textContent = textElements[lang].counselingServicesTitle;
      featuredServicesDescriptions[1].textContent = textElements[lang].counselingServicesDesc;
      featuredServicesTitles[2].textContent = textElements[lang].legalAssistanceTitle;
      featuredServicesDescriptions[2].textContent = textElements[lang].legalAssistanceDesc;
    }

    // Emergency section
    const emergencyTitle = document.querySelector('#emergency .section-title h2');
    const emergencyDesc = document.querySelector('#emergency .section-title p');
    if (emergencyTitle) emergencyTitle.textContent = textElements[lang].emergencyHelplinesTitle;
    if (emergencyDesc) emergencyDesc.textContent = textElements[lang].emergencyHelplinesDesc;
    const gvFundTitle = document.querySelector('#emergency .info-item h3:nth-of-type(1)');
    const gvFundCall = document.querySelector('#emergency .info-item p:nth-of-type(1)');
    const gvFundDesc = document.querySelector('#emergency .info-item p:nth-of-type(2)');
    if (gvFundTitle) gvFundTitle.textContent = textElements[lang].genderViolenceRecoveryFund;
    if (gvFundCall) gvFundCall.textContent = textElements[lang].genderViolenceRecoveryFundCall;
    if (gvFundDesc) gvFundDesc.textContent = textElements[lang].genderViolenceRecoveryFundDesc;
    const befriendersTitle = document.querySelector('#emergency .info-item h3:nth-of-type(2)');
    const befriendersCall = document.querySelector('#emergency .info-item p:nth-of-type(3)');
    const befriendersDesc = document.querySelector('#emergency .info-item p:nth-of-type(4)');
    if (befriendersTitle) befriendersTitle.textContent = textElements[lang].befriendersKenya;
    if (befriendersCall) befriendersCall.textContent = textElements[lang].befriendersKenyaCall;
    if (befriendersDesc) befriendersDesc.textContent = textElements[lang].befriendersKenyaDesc;
  }

  languageLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const lang = e.target.getAttribute('data-lang');
      setLanguage(lang);
    });
  });

  // Set default language to English
  setLanguage('en');

})();
