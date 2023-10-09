// calendar overview page

let calendar = document.querySelector('.calender')

const month_names = ['Januari', 'Februari', 'Maart', 'April', 'Mei', 'Juni', 'Juli', 'Augustus', 'September', 'Oktober', 'November', 'December']

function isLeapYear  (year) {
    return (year % 4 === 0 && year % 100 !== 0 && year % 400 !== 0) || (year % 100 === 0 && year % 400 ===0)
}

function getFebDays  (year) {
    return isLeapYear(year) ? 29 : 28
}

function generateCalendar (month, year) {
    
    let calendar_days = calendar.querySelector('.calendar-days')
    let calendar_header_year = calendar.querySelector('#year')

    let days_of_month = [31, getFebDays(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    calendar_days.innerHTML = ''

    let currentDate = new Date()
    if (month > 11 || month < 0) month = currentDate.getMonth()
    if (!year) year = currentDate.getFullYear()

    let current_month = `${month_names[month]}`
    month_picker.innerHTML = current_month
    calendar_header_year.innerHTML = year

    // get first day of the month

    let first_day = new Date(year, month, 1)

    for (let i = 0; i <= days_of_month[month] + first_day.getDay() - 1; i++) {
        let day = document.createElement('div')
        if (i >= first_day.getDay()) {
            day.classList.add('calendar-day-hover')
            day.innerHTML = i - first_day.getDay() + 1
            day.innerHTML += `<span></span>
                            <span></span>
                            <span></span>
                            <span></span>`
            if (i - first_day.getDay() + 1 === currentDate.getDate() && year === currentDate.getFullYear() && month === currentDate.getMonth()) {
                day.classList.add('curr-date')
            }

        }
        calendar_days.appendChild(day)
    }    
}

let month_list = calendar.querySelector('.month-list')

month_names.forEach((e, index) => {
    let month = document.createElement('div')
    month.innerHTML = `<div data-month="${index}">${e}</div>`
    month.querySelector('div').onclick = () => {
        month_list.classList.remove('show')
        current_month.value = index
        generateCalendar(index, current_year.value)
    }
    month_list.appendChild(month)
})

let month_picker  = calendar.querySelector('#month-picker')

month_picker.onclick = () => {
    month_list.classList.add('show')    
}

let currentDate = new Date()

let current_month = {value: currentDate.getMonth()}
let current_year = {value: currentDate.getFullYear()}

generateCalendar(current_month.value, current_year.value)

document.querySelector('#prev-year').onclick = () => {
    --current_year.value
    generateCalendar(current_month.value, current_year.value)
}

document.querySelector('#next-year').onclick = () => {
    --current_year.value
    generateCalendar(current_month.value, current_year.value)
}

