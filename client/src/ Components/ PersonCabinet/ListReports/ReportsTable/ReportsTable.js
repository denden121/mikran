import React from "react"
import {Modal} from "antd"

const Report =(props)=>{
    let a = []
    for(let i of props.reports){
        // console.log('i',i)
        a.push({name:i.name,
                code:i.code,
                pk:i.pk})
        a.push(i.users)
    }

    // console.log('a',a)
    return a.map((item,key)=>{
        // console.log('item',item)
        console.log(item.users)
        return Array.isArray( item)? item.map((user)=> {
                return <tr>
                    <td scope="row"></td>
                    <td></td>
                    <td><a onClick={props.onClickShowModal} style={{cursor: "pointer"}}>user.name</a></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
            })
            : <tr>
                <td colSpan="7" scope="colgroup" className="table-secondary">Отдел</td>
            </tr>
    })
}

const ReportsTable =(props)=>{
    return(
        <div className="table-responsive">
            <table className="table table-bordered table-sm">
                <thead>
                    <tr>
                        <th scope="col">№ п/п</th>
                        <th scope="col">ФИО</th>
                        <th scope="col">Отчет*</th>
                        <th scope="col">Норма</th>
                        <th scope="col">Orion</th>
                        <th scope="col">Проверил</th>
                        <th scope="col">Блокировал</th>
                    </tr>
                </thead>
                <tbody>
                    <Report reports ={props.reports}/>
                </tbody>
            </table>
        </div>
    )
}

export default ReportsTable