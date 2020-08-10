import React from "react"
import CardModal from "./CardModal/CardModal"

const Workers = (props) =>{
    let workers = Array.from(props.workers)
    console.log(workers)
    return workers.map((worker,index)=>{
        console.log(worker)
        return(
            <tr>
                <th scope="row">1</th>
                <td>{worker.person['№ db']}</td>
                <td><a onClick={props.onClickPerson} style={{cursor:"pointer"}}>{worker.person.full_name}</a></td>
                <td>{worker.person.date}</td>
                <td>{worker.person.shift}</td>
                <td>{worker.person.SRI_SAS ? 'да' : 'нет'}</td>
                <td>{worker.person.ockladnaya}</td>
                <td>{worker.person.groups.join(' ')}</td>
                <td>{worker.person.position}</td>
            </tr>
        )
})

}

const ListEmp =(props)=>{
    return(
        <div className="row">
            <div className="col-sm-12 col-md-12 col-lg-12">
            <table class="table table-bordered">
                <thead>
                    <tr>
                    <th scope="col">№ БД</th>
                    <th scope="col">№ 1С</th>
                    <th scope="col">ФИО</th>
                    <th scope="col">Дата труд-ва</th>
                    <th scope="col">Смена</th>
                    <th scope="col">НИИСЭС</th>
                    <th scope="col">Окладная СОТ</th>
                    <th scope="col">Группы</th>
                    <th scope="col">Подразделения,должность</th>
                    </tr>
                </thead>
                <tbody>
<<<<<<< HEAD
                    <Workers workers={props.workers}/>
=======
                    <tr>
                    <th scope="row">1</th>
                    <td>1</td>
                    <td><a href="#" onClick={props.onClickShowModal} style={{cursor:"pointer"}}>Осеева Анастасия Михайловна</a></td>
                    <td>12.02.2020</td>
                    <td>папрпа</td>
                    <td>иапиа</td>
                    <td>пвдлпо</td>
                    <td>пвапвп</td>
                    <td>пиаиапи</td>
                    </tr>                                       
>>>>>>> origin/Deploy
                </tbody>
                </table>
            </div>
        </div>
    )
}

export default ListEmp