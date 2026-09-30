// Arabic UI layer for the TICVAI prototypes. When any element carries dir="rtl",
// visible text, placeholders and labels inside it are swapped for Arabic; switching
// back restores the English. Proper names (venues, shows, dishes) stay as written.
(function () {
  if (window.__tvAr) return; window.__tvAr = true;
  const D = {
    "Dubai · 5 venues": "دبي · 5 أماكن", "You're at Summit Peaks": "أنت في Summit Peaks", "At venue mode is live — map, queue, orders": "وضع المكان مفعّل — الخريطة والطابور والطلبات", "Open · 1.4k left today": "مفتوح · متبقٍ 1.4 ألف اليوم", "Selling fast tonight": "تُباع بسرعة الليلة", "Weekend sold out": "نفدت عطلة نهاية الأسبوع", "Six productions": "ستة عروض", "Tables from 19:00": "طاولات من 19:00", "Open-dated · use within 90 days": "تاريخ مفتوح · تُستخدم خلال 90 يومًا", "Any 2 days within a month": "أي يومين خلال شهر", "Emirates ID required": "الهوية الإماراتية مطلوبة", "Best value": "أفضل قيمة", "Residents": "المقيمون", "Min 1.10 m for the big rides": "1.10 م حدًا أدنى للألعاب الكبيرة", "Under 3s free": "مجانًا لمن هم دون 3 سنوات", "Emirates ID": "الهوية الإماراتية", "1 day": "يوم واحد", "Free adult entry": "دخول مجاني للبالغين", "Most popular": "الأكثر شعبية", "Selling fast": "تُباع بسرعة", "Choose a date": "اختر تاريخًا", "Select your date": "اختر تاريخك", "Pick a date": "اختر تاريخًا", "Pick your day": "اختر يومك", "Select a date": "اختر تاريخًا", "Your basket": "سلتك", "Your cart": "سلتك", "Nothing added yet. Pick your fixture to start.": "لم تتم إضافة شيء بعد. اختر مباراتك للبدء.", "Tap a section to zoom in. Every dot is a seat: coloured by price, grey when taken. Tap dots to pick seats.": "اضغط على قسم للتكبير. كل نقطة مقعد: ملونة حسب السعر ورمادية إذا كانت محجوزة. اضغط النقاط لاختيار المقاعد.", "Pitch": "الملعب", "Stage": "المسرح", "Sport": "رياضة", "Concert": "حفلة", "Scan": "مسح", "Light": "فاتح", "Dark": "داكن", "Auto": "تلقائي", "Upcoming 3": "3 قادمة", "Gold member · 4,340 points": "عضو ذهبي · 4,340 نقطة", "Visa ending 4242": "فيزا تنتهي بـ 4242", "Sign in or create an account": "سجّل الدخول أو أنشئ حسابًا", "Use your TICVAI account": "استخدم حساب TICVAI", "One-time, no password": "لمرة واحدة، دون كلمة مرور", "Continue to payment": "المتابعة إلى الدفع", "Choose how to check out": "اختر طريقة الدفع", "Sign in to continue": "سجّل الدخول للمتابعة", "Not me – keep separate": "ليس أنا – أبقه منفصلًا", "Soft": "مرن", "Hard": "نهائي", "Again": "مجددًا", "Paid": "مدفوع", "Declined": "مرفوض", "Back": "رجوع", "Apple Pay": "Apple Pay", "Mastercard ending 8812": "ماستركارد تنتهي بـ 8812",
    'Search': 'بحث', 'Sign in': 'تسجيل الدخول', 'Sign out': 'تسجيل الخروج', 'Create account': 'إنشاء حساب', 'Close': 'إغلاق',
    'Read more': 'اقرأ المزيد', 'Less': 'أقل', 'Add': 'إضافة', 'Remove': 'إزالة', 'Apply': 'تطبيق', 'Empty': 'إفراغ', 'Keep': 'إبقاء',
    'Continue': 'متابعة', 'Book': 'احجز', 'Book now': 'احجز الآن', 'Buy tickets': 'اشترِ التذاكر', 'Book tickets': 'احجز التذاكر', 'Get tickets': 'احصل على التذاكر',
    'Book a table': 'احجز طاولة', 'Book a visit': 'احجز زيارة', 'Book a session': 'احجز جلسة', 'Reserve a seat': 'احجز مقعدًا', 'Book a place': 'احجز مكانًا',
    'Subtotal': 'المجموع الفرعي', 'VAT 5%': 'ضريبة القيمة المضافة 5%', 'Total': 'الإجمالي', 'Estimate': 'تقدير', 'Due now': 'المستحق الآن',
    'Back a step': 'خطوة للخلف', 'View': 'عرض', 'Resume': 'استئناف', 'See all': 'عرض الكل', 'Clear': 'مسح', 'Today': 'اليوم', 'Live': 'مباشر',
    'Tickets from': 'التذاكر من', 'Tickets': 'التذاكر', 'My tickets': 'تذاكري', 'Used': 'مستخدمة', 'When': 'متى', 'Party': 'المجموعة', 'Entry': 'الدخول',
    'Manage': 'إدارة', 'Help centre': 'مركز المساعدة', 'Your cases': 'طلباتك', 'Reply': 'رد', 'Full name': 'الاسم الكامل', 'Six-digit code': 'رمز من ست خانات',
    'Send a new code': 'أرسل رمزًا جديدًا', 'Email': 'البريد الإلكتروني', 'or': 'أو', 'Continue with Apple': 'المتابعة مع Apple', 'Continue with Google': 'المتابعة مع Google',
    'Continue with UAE Pass': 'المتابعة مع الهوية الرقمية', 'Preview state': 'معاينة الحالة', 'Remove this guest': 'إزالة هذا الضيف', 'Reference': 'المرجع',
    'Manage this booking': 'إدارة هذا الحجز', 'Powered by': 'مدعوم من', 'Secure checkout': 'دفع آمن', 'Results': 'النتائج', 'Recent searches': 'عمليات البحث الأخيرة',
    'Popular searches': 'الأكثر بحثًا', 'Featured categories': 'فئات مميزة', 'Add to booking': 'أضف إلى الحجز', 'Directions': 'الاتجاهات', 'From': 'من', 'To': 'إلى',
    'Your order': 'طلبك', 'Wishlist': 'المفضلة', 'Terms': 'الشروط', 'Privacy': 'الخصوصية', 'Refunds': 'الاسترداد', 'Contact': 'تواصل معنا', 'Accessibility': 'إمكانية الوصول',
    'Support': 'الدعم', 'Talk to a person': 'تحدث إلى موظف', 'Parking': 'مواقف السيارات', 'Loyalty': 'الولاء', 'Alerts': 'التنبيهات', 'Order food': 'اطلب الطعام',
    'Virtual queue': 'الطابور الافتراضي', 'Map & waits': 'الخريطة وأوقات الانتظار', 'Shop & drop': 'تسوّق واستلم', 'Redeem': 'استبدال', 'Allergens': 'مسببات الحساسية',
    'Adult': 'بالغ', 'Child': 'طفل', 'Senior': 'كبار السن', 'Infant': 'رضيع', 'Guest': 'ضيف', 'Guests': 'الضيوف', 'Companion': 'مرافق',
    'Single day': 'يوم واحد', 'Two-day flexible': 'يومان مرنان', 'UAE resident': 'مقيم في الإمارات', 'Dated day pass': 'تذكرة يوم بتاريخ', 'Day pass': 'تذكرة يوم',
    'Fast Track': 'المسار السريع', 'Season ticket': 'تذكرة الموسم', 'Full season': 'الموسم الكامل', 'Half season': 'نصف موسم', 'Gift card': 'بطاقة هدية',
    'Silver': 'فضي', 'Gold': 'ذهبي', 'Platinum': 'بلاتيني', 'Premium': 'مميز', 'Standard': 'عادي', 'Economy': 'اقتصادي', 'Suite': 'جناح', 'Seated': 'جلوس', 'Standing': 'وقوف', 'Zone': 'منطقة',
    'VIP Box': 'مقصورة كبار الشخصيات', 'Lower Tier': 'المدرج السفلي', 'Upper Tier': 'المدرج العلوي', 'North End': 'الطرف الشمالي', 'Family Stand': 'مدرج العائلات',
    'Choose your section': 'اختر القسم', 'Choose your seats': 'اختر مقاعدك', 'Choose your zone': 'اختر المنطقة', 'Whole bowl': 'الملعب كاملًا', 'Whole map': 'الخريطة كاملة',
    'Zone pricing': 'أسعار المناطق', 'STAGE': 'المسرح', 'Sight line': 'مجال الرؤية', 'Payment method': 'طريقة الدفع', 'Card holder': 'حامل البطاقة', 'Card number': 'رقم البطاقة',
    'Expiry': 'تاريخ الانتهاء', 'Name on card': 'الاسم على البطاقة', 'Add to Apple Wallet': 'أضف إلى Apple Wallet', 'Download PDF': 'تنزيل PDF', 'Email again': 'أرسل البريد مجددًا',
    'Reissue QR': 'إعادة إصدار الرمز', 'Transfer tickets': 'تحويل التذاكر', 'Save changes': 'حفظ التغييرات', 'Start over': 'ابدأ من جديد', 'Select this': 'اختر هذا',
    'Select tickets': 'اختر التذاكر', 'Select your tickets': 'اختر تذاكرك', 'Choose your ticket': 'اختر تذكرتك', 'Choose your session': 'اختر جلستك', 'Your fixture': 'مباراتك',
    'Choose your show': 'اختر العرض', 'Plan your visit': 'خطط لزيارتك', 'Choose your membership': 'اختر عضويتك', 'Skip the queue': 'تخطَّ الطابور', 'Seats': 'المقاعد',
    'Extras': 'الإضافات', 'Your details': 'بياناتك', 'Payment': 'الدفع', 'Confirmed': 'تم التأكيد', 'Fixture': 'المباراة', 'Session': 'الجلسة', 'Booking': 'الحجز', 'Visit': 'الزيارة',
    'Membership': 'العضوية', 'Memberships': 'العضويات', 'Section': 'القسم', 'Table': 'الطاولة', 'Menu': 'القائمة', 'Order': 'الطلب', 'Offers': 'العروض', 'Offer': 'عرض',
    'Discover': 'استكشف', 'At the venue': 'في المكان', 'At venue': 'في المكان', 'Help': 'المساعدة', 'Account': 'الحساب', 'Account overview': 'نظرة عامة على الحساب', 'Wallet': 'المحفظة',
    'Payment methods': 'طرق الدفع', 'Personal details': 'البيانات الشخصية', 'Security': 'الأمان', 'Queue now': 'الطابور الآن', 'Status': 'الحالة', 'Height rule': 'شرط الطول',
    'Live as of': 'مباشر منذ', 'Upcoming': 'القادمة', 'Past': 'السابقة', 'Add to wallet': 'أضف إلى المحفظة', 'Save PDF': 'حفظ PDF', 'Reschedule': 'إعادة الجدولة',
    'Add guests': 'إضافة ضيوف', 'Transfer ticket': 'تحويل التذكرة', 'Request a refund': 'طلب استرداد', 'Cancel booking': 'إلغاء الحجز', 'Call the venue': 'اتصل بالمكان',
    'Overview': 'نظرة عامة', 'Saved guests': 'الضيوف المحفوظون', 'Wallet & gift cards': 'المحفظة وبطاقات الهدايا', 'Order history': 'سجل الطلبات', 'Notifications': 'الإشعارات',
    'Reservations': 'الحجوزات', 'Newsletters': 'النشرات البريدية', 'Data & privacy': 'البيانات والخصوصية', 'Billing': 'الفوترة', 'Billing statement': 'كشف الفواتير',
    'Edit details': 'تعديل البيانات', 'Done': 'تم', 'Loading': 'جارٍ التحميل', 'Change': 'تغيير', 'Confirm and pay': 'تأكيد والدفع', 'Pay': 'ادفع', 'Card': 'بطاقة',
    'Good availability': 'توفر جيد', 'Limited': 'محدود', 'Sold out': 'نفدت', 'Next seven days': 'الأيام السبعة القادمة', 'Book ahead': 'احجز مسبقًا', 'Save & exit': 'حفظ وخروج',
    'Date & tickets': 'التاريخ والتذاكر', 'Pick your section': 'اختر قسمك', 'Checkout entry': 'بدء الدفع', 'Guest checkout': 'الدفع كضيف', 'Continue as guest': 'المتابعة كضيف',
    'Email me a code': 'أرسل لي رمزًا', 'Verify': 'تحقق', 'The code is six digits.': 'الرمز مكوّن من ست خانات.', 'We found a profile that matches': 'وجدنا ملفًا مطابقًا',
    'Use this profile': 'استخدم هذا الملف', 'Membership billing': 'فوترة العضوية', 'Renew automatically': 'تجديد تلقائي', 'Delete my account': 'حذف حسابي',
    "You're going": 'حجزك مؤكد', 'Set a password': 'عيّن كلمة مرور', 'Open my tickets': 'افتح تذاكري', 'Back to discover': 'العودة إلى الاستكشاف', 'Show at gate': 'اعرضها عند البوابة',
    'Engine settings': 'إعدادات المحرك', 'Reset': 'إعادة ضبط', 'Pay with Apple Pay': 'ادفع عبر Apple Pay', 'Where to': 'إلى أين', 'Tonight': 'الليلة', 'Evening, Layla': 'مساء الخير، ليلى',
    'Search venues, events, dining': 'ابحث عن الأماكن والفعاليات والمطاعم', 'Seat map': 'خريطة المقاعد', 'Settings': 'الإعدادات', 'All screens': 'كل الشاشات',
    'Retry now': 'أعد المحاولة الآن', 'Use another card': 'استخدم بطاقة أخرى', 'Declined again': 'رُفضت مجددًا', 'Your membership continues': 'عضويتك مستمرة', 'Choose a card': 'اختر بطاقة',
    'Check who can take part': 'تحقق من المؤهلين للمشاركة', 'Choose another activity': 'اختر نشاطًا آخر', 'Can take part': 'يمكنه المشاركة', 'Accompanying adult': 'بالغ مرافق',
    'Age': 'العمر', 'Height': 'الطول', 'Pupils': 'الطلاب', 'Children': 'الأطفال', 'Send request': 'أرسل الطلب', 'Pick another date': 'اختر تاريخًا آخر',
    'Check your delivery': 'تحقق من التوصيل', 'Delivery fee': 'رسوم التوصيل', 'Delivery': 'توصيل', 'Takeaway': 'استلام', 'Dine in': 'تناول في المطعم', 'Emirate': 'الإمارة',
    'Change address': 'تغيير العنوان', 'Switch to takeaway': 'التحويل إلى الاستلام', 'That time just filled': 'امتلأ هذا الوقت للتو', 'Below the minimum order': 'أقل من الحد الأدنى للطلب',
    'Pay without an account': 'ادفع دون حساب', 'Send code': 'أرسل الرمز', 'Enter the six-digit code': 'أدخل الرمز المكوّن من ست خانات', 'Verify code': 'تحقق من الرمز',
    'Continue as a new guest': 'المتابعة كضيف جديد', 'Matched on': 'تطابق عبر', 'Past orders': 'الطلبات السابقة', 'First order': 'أول طلب', 'Profile type': 'نوع الملف',
    'Everything': 'الكل', 'Theme park': 'مدينة ملاهٍ', 'Water park': 'حديقة مائية', 'Stadium': 'ملعب', 'Theatre': 'مسرح', 'Dining': 'مطاعم', 'Play & workshops': 'اللعب وورش العمل',
    'What\u2019s on': 'الفعاليات', 'Offers & promotions': 'العروض والترويج', 'Contact & venue info': 'التواصل ومعلومات المكان', 'Language': 'اللغة', 'Log in': 'تسجيل الدخول', 'Register': 'التسجيل',
    'Upgrade your day': 'طوّر يومك', 'Your booking': 'حجزك', 'Your seats': 'مقاعدك', 'Your reservation': 'حجزك', 'Date of visit': 'تاريخ الزيارة', 'Nothing added yet.': 'لم تتم إضافة شيء بعد.',
    'Choose seats': 'اختر المقاعد', 'Checkout': 'الدفع', 'Sign in to pay': 'سجّل الدخول للدفع', 'Another date?': 'تاريخ آخر؟', 'Kick-off': 'انطلاق المباراة', 'Gates open': 'فتح البوابات',
    'Monthly membership': 'عضوية شهرية', 'Opening hours': 'ساعات العمل', 'Getting here': 'الوصول إلينا', 'Address': 'العنوان', 'Phone': 'الهاتف', 'Call': 'اتصال', 'Message': 'رسالة',
    'Mobile': 'الجوال', 'Nationality': 'الجنسية', 'Consent': 'الموافقة', 'Marketing': 'التسويق', 'Signature': 'التوقيع', 'Notes': 'ملاحظات', 'Occasion': 'المناسبة', 'Company': 'الشركة'
  };
  const R = [
    [/^Step (\d+) of (\d+)$/i, 'الخطوة $1 من $2'], [/^from AED ([\d,.]+)$/, 'من $1 درهم'], [/^AED ([\d,.]+)$/, '$1 درهم'], [/^AED ([\d,.]+)\+$/, '+$1 درهم'],
    [/^(\d+) tickets? · Visit (.+)$/, '$1 تذاكر · الزيارة $2'], [/^View from (.+)$/, 'المنظر من $1'], [/^Question (\d) of (\d)$/, 'السؤال $1 من $2'], [/^Section (.+)$/, 'القسم $1'],
    [/^(\d+) min queue now$/, 'انتظار $1 دقيقة الآن'], [/^Walk on$/, 'دون انتظار'], [/^Pay deposit (.+)$/, 'ادفع العربون $1'], [/^Valid (\d+) days$/, 'صالحة $1 يومًا'], [/^(\d+) days?$/, '$1 أيام'],
    [/^(\d+) Hours?$/i, '$1 ساعات'], [/^Min ([\d.]+) m$/, 'الحد الأدنى $1 م'], [/^Min (\d+) cm$/, 'الحد الأدنى $1 سم']
  ];
  if (window.TV_AR_EXTRA) Object.assign(D, window.TV_AR_EXTRA);
  window.__tvArD = D;
  if (window.TV_AR_RULES) window.TV_AR_RULES.forEach(r => R.push(r));
  const miss = window.__tvArMiss = new Set();
  const map = new WeakMap(), touched = new Set();
  const tr = v => {
    const k = v.trim(); if (!k || /[\u0600-\u06FF]/.test(k)) return null;
    if (D[k]) return v.replace(k, D[k]);
    for (const [re, rep] of R) if (re.test(k)) return v.replace(k, k.replace(re, rep));
    if (/[A-Za-z]{2}/.test(k)) miss.add(k);
    return null;
  };
  const ATTR = ['placeholder', 'aria-label', 'title'];
  function pass() {
    const roots = [...document.querySelectorAll('[dir="rtl"]')];
    const on = roots.length > 0;
    if (!on) { touched.forEach(n => { const r = map.get(n); if (!r) return; if (r.attr) { if (n.getAttribute(r.attr) === r.out) n.setAttribute(r.attr, r.src); } else if (n.nodeValue === r.out) n.nodeValue = r.src; map.delete(n); }); touched.clear(); return; }
    roots.forEach(root => {
      const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      let n; while ((n = w.nextNode())) {
        const v = n.nodeValue, r = map.get(n);
        if (r && v === r.out) continue;
        const t = tr(v); if (t && t !== v) { map.set(n, { src: v, out: t }); touched.add(n); n.nodeValue = t; }
      }
      root.querySelectorAll('[placeholder],[aria-label],[title]').forEach(el => ATTR.forEach(a => {
        const v = el.getAttribute(a); if (!v) return; const key = el; const r = map.get(key);
        if (r && r.attr === a && v === r.out) return;
        const t = tr(v); if (t && t !== v) { map.set(key, { attr: a, src: v, out: t }); touched.add(key); el.setAttribute(a, t); }
      }));
    });
  }
  window.__tvArPass = pass;
  let q = 0; const sched = () => { if (q) return; q = setTimeout(() => { q = 0; try { pass(); } catch (e) { console.warn('ar-err ' + (e && e.stack || e)); } }, 30); };
  const start = () => { new MutationObserver(sched).observe(document.body, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ['dir'] }); sched(); };
  if (document.body) start(); else document.addEventListener('DOMContentLoaded', start);
})();
