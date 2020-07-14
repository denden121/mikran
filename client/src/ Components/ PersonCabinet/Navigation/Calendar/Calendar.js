import React from "react"
import "./Calendar.css"

class Calendar extends React.Component{
    // datepickerFactory($);
    // datepickerJAFactory($);
    // $(function () {
    //     $('#datetimepicker10').datetimepicker({
    //         viewMode: 'years',
    //         format: 'MM/YYYY'
    //     });
    // });
    render(){
        return(
            <div className="calendar">
                <div className="year align-center rounded">
                    <ul>
                        <li className="prev">&#10094;</li>
                        <li className="next">&#10095;</li>
                        <li><span style={{fontSize:"18px"}}>2020</span></li>
                    </ul>
                </div>
                <div>
                    <div className="winter border rounded">Дек</div>
                    <div className="winter border rounded">Янв</div>  
                    <div className="winter border rounded">Фев</div>  
                </div>
                <div>
                    <div className="spring border rounded">Март</div>
                    <div className="spring border rounded">Апр</div>
                    <div className="spring border rounded">Май</div>
                </div> 
                <div>
                    <div className="summer border rounded">Июнь</div>
                    <div className="summer border rounded">Июль</div>
                    <div className="summer border rounded">Авг</div>
                </div>  
                <div>
                    <div className="autumn border rounded">Сен</div>
                    <div className="autumn border rounded">Окт</div>
                    <div className="autumn border rounded">Ноя</div>
                </div>   
            </div>            
        )
    }
const Calendar = (props) =>{
    return(
        <div className="Calendar">
            <div>
                <div onClick={props.onClickDate} className="winter border">Дек</div>
                <div onClick={props.onClickDate} className="winter border">Янв</div>
                <div onClick={props.onClickDate} className="winter border">Фев</div>
            </div>
            <div>
                <div onClick={props.onClickDate} className="spring border">Март</div>
                <div onClick={props.onClickDate} className="spring border">Апр</div>
                <div onClick={props.onClickDate} className="spring border">Май</div>
            </div>
            <div>
                <div onClick={props.onClickDate} className="summer border">Июнь</div>
                <div onClick={props.onClickDate} className="summer border">Июль</div>
                <div onClick={props.onClickDate} className="summer border">Авг</div>
            </div>
            <div>
                <div onClick={props.onClickDate} className="autumn border">Сен</div>
                <div onClick={props.onClickDate} className="autumn border">Окт</div>
                <div onClick={props.onClickDate} className="autumn border">Ноя</div>
            </div>
        </div>
    )
}

export default Calendar