import React from "react"
import "./Norma.css"

const Norma = (props) => {
    return(
        <div className="norma">
            <div className="row no-gutters flex-md-row mb-4  h-md-250 position-relative">
                 <div className="card col-md-3">
                    <div className="card-header text-left ">
                        Норма рабочих дней за месяц
                    </div>
                    <div className="card-body text-left">
                        <div className="input-group">
                            <input type="text" className="form-control" style={{padding:"0",margin:"0"}} />
                        </div>
                    </div>
                </div>
                <div className="card col-md-3">
                    <div className="card-header text-left ">
                        Норма рабочих часов за месяц
                    </div>
                    <div className="card-body text-left">
                        <div className="input-group">
                            <input type="text" className="form-control" style={{padding:"0",margin:"0"}} />
                        </div>
                    </div>
                </div>
                <div className="card col-md-3">
                    <div className="card-header text-left ">
                        Время изменения таблицы другим пользователем
                    </div>
                    <div className="card-body text-left">
                        <div className="input-group">
                            <input type="text" className="form-control" style={{padding:"0",margin:"0"}} />
                        </div>
                    </div>
                </div>
            </div>
            {/* <br/> */}
            {/* <div className="row no-gutters flex-md-row mb-4  h-md-250 position-relative">
                <div className="card col-md-4">
                    <div className="card-header text-left bg-success">
                        Время изменения таблицы другим пользователем
                    </div>
                    <div className="norma card-body text-left">
                        Соединение открыто
                    </div>
                </div>
            </div> */}
        </div>
    )
}

export default Norma