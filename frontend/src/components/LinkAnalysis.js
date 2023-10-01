import {useRef, useState, useEffect} from "react";
import "./LinkAnalysis.css";

// const DOMMY_DATA = {
//   "سلامت خانواده": {
//       "page_rank": {
//           "tops": [
//               "جوش شیرین به عنوان شامپو خشک: اگر پوست سرتان خیلی چرب است و زمانی برای شستن موها ندارید، می‌توانید به سادگی از جوش شیرین استفاده کنید و مصرف محصولات مضر حاوی مواد شیمیایی را کاهش دهید.",
//               "برای اینکه بتوانید در طول روز انرژی بیشتری داشته باشید و انرژی خود را صرف کارهای خلاقانه کنید لازم است از میوه جات و سبزیجات زیادی در رژیم غذاییتان استفاده کنید تا تاثیرات آن را روی بدن تان ببینید.",
//               "درست است که هفته‌ای یک بار دویدن و روزی نیم ساعت پیاده رفتن عمر شما را طولانی می‌کند اما محققان می‌گویند اگر تنها ۳۰دقیقه زمان ثابت را به ورزش کردن اختصاص دهید، عمرتان ۱۵سال طولانی‌تر می‌شود."
//           ],
//           "bottoms": [
//               "به تعویق انداختن زمان بیولوژیک بدن، از لحاظ علمی امکان پذیر است.",
//               "پیاده روی بهترین روش فعالیت کردن برای افراد سالمند است.",
//               "این در حالی است که بی تحرکی برای سلامت آنها بسیار مضر بوده و باید ساعاتی را از منزل خارج شوند."
//           ]
//       },
//       "hits": {
//           "Authorities": {
//               "tops": [
//                   "جایگزین کردن مواد شوینده با جایگزین کردن و استفاده از مواد شوینده دوستدار محیط زیست می‌توانید میزان آلودگی هوای داخل خانه را کاهش داده، خطر ابتلا به بیماریهای آسم و آلرژی را کم کنید.",
//                   "این کار ساده از انتشار آلودگی‌های بیرون مانند آلودگی‌های ناشی از خودروها، مواد شیمیایی و افت کش‌ها در داخل خانه جلوگیری می‌کند.",
//                   "فراموش نکنید که اصلا از جاروبرقی برای تمیز کردن محل استفاده نکنید چراکه باعث پخش آلودگی در هوای محیط شود."
//               ],
//               "bottoms": [
//                   "عامل مشخصی خواب شما را مختل می‌کند: صدای دزدگیر ماشین همسایه، فرزندی که در حال دندان درآوردن است، استفاده از داروهای استروئیدی، نگرانی‌های شغلی و … هیچ کس دوست ندارد خوابش را از دست بدهد.",
//                   "این متخصص داخلی در پایان از همه افراد خواست تا با توجه به این مسئله بیش از پیش هوای پدران را داشته و سعی کنند در زمینه استفاده از کولر شرایط فیزیولوژیکی بدن آنها را در نظر بگیرند.",
//                   "رنگ لعابی پودری را روی نشاسته بپاشید و بگذارید کودک ترکیب رنگ‌‌ها را تجربه کند."
//               ]
//           },
//       }
//   }
// }

const LinkAnalysis = () => {
    const [isFormSubmitted, setIsFormSubmitted] = useState(false);
    const [isHitsSelected, setIsHitsSelected] = useState(false);
    const [data, setData] = useState({});
    const [selectedData, setSelectedData] = useState({});
    const categoryInputRef = useRef();
    const methodInputRef = useRef();
    const hitsInputRef = useRef();

    const formSubmissionHandler = (event) => {
        event.preventDefault();
        selectData();
        setIsFormSubmitted(true);
    };

    const selectData = () => {
        const category = categoryInputRef.current.value;
        const method = methodInputRef.current.value;
        if (method === 'page_rank') {
            setSelectedData(data[category][method])
        } else {
            setSelectedData(data[category][method][hitsInputRef.current.value]);
        }
    }

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch(
                "http://127.0.0.1:8000/api/v1/health/link_analyser/"
            );
            const json = await response.json();
            setData(json);
        };
        fetchData();
    }, []);

    const selectHits = () => {
        if (document.getElementById('linkmethod').value === 'hits') {
            setIsHitsSelected(true);
        }else {
            setIsHitsSelected(false);
        }
    };

    return (
        <>
            <div className="form_container">
                <form onSubmit={formSubmissionHandler}>
                    <label>Category</label>
                    <select ref={categoryInputRef} id="category" name="category">
                        <option value="سلامت خانواده">سلامت خانواده</option>
                        <option value="تازه های سلامت">تازه‌های سلامت</option>
                        <option value="پیشگیری و بیماریها">پیشگیری و بیماری‌ها</option>
                        <option value="سلامت جنسی">سلامت جنسی</option>
                        <option value="تغذیه">تغذیه</option>
                        <option value="سلامت روان">سلامت روان</option>
                        <option value="متخصصین">متخصصین</option>
                        <option value="پوست و مو">پوست و مو</option>
                        <option value="دهان و دندان">دهان و دندان</option>
                    </select>
                    <label>Method</label>
                    <select onChange={selectHits} ref={methodInputRef} id="linkmethod" name="method">
                        <option value="page_rank">Page Rank</option>
                        <option value="hits">Hits</option>
                    </select>
                    {isHitsSelected && (
                        <select className="hits-selection" ref={hitsInputRef}>
                            <option value="Authorities">Authorities</option>
                            <option value="Hubs">Hubs</option>
                        </select>
                    )}
                    <button type='submit'>search</button>
                </form>
            </div>
            {isFormSubmitted && (
                <>
                    <div className='link-analysis_container'>
                        <h4 className="link-analysis_title">مرتبط ‌ترین جملات</h4>
                        <div className="sentences_container">
                            {selectedData["tops"].map((item, index) => <p key={index}>{item}</p>)}
                        </div>
                    </div>
                    <div className='link-analysis_container'>
                        <h4 className="link-analysis_title">نامرتبط‌ ترین جملات</h4>
                        <div className="sentences_container">
                            {selectedData["bottoms"].map((item, index) => <p key={index}>{item}</p>)}
                        </div>
                    </div>
                </>
            )}
        </>
    )

};

export default LinkAnalysis;
