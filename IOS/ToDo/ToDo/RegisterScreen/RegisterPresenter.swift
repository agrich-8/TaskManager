import Foundation

final class RegisterPresenter:ViewToPresenterRegisterProtocol {
    var view: PresenterToViewRegisterProtocol?
    var router: PresenterToRouterRegisterProtocol?
    var interactor: PresenterToInteractorRegisterProtocol?
    var user = RegisterUser(login: "", mail: "", password: "")
    
    func setLogin(login: String?) {
        guard let login = login, login != "" && login != " " else {
            view?.errorRegister(errorText: "Login isnt correct")
            user.login = ""
            return
        }
        self.user.login = login
        print(user)
    }
    
    func setMail(mail: String?) {
        guard let mail = mail, mail != "" && mail != " " else {
            view?.errorRegister(errorText: "Mail isnt correct")
            user.mail = ""
            return
        }
        self.user.mail = mail
        print(user)
    }
    
    func setPassword(password: String?) {
        guard let password = password, password != "" && password != " " else {
            view?.errorRegister(errorText: "Password isnt correct")
            user.password = ""
            return
        }
        self.user.password = password
        print(user)
    }
    
    
    func checkConfirmPassword(confirmPassword: String?) {
        guard let confirmPassword = confirmPassword,confirmPassword != "" && confirmPassword != " " && confirmPassword == self.user.password else {
            view?.errorSimilarPassword()
            return
        }
        view?.enableConfirmButton()
    }
    
    func userTapConfirmButton() {
        interactor?.registeringUser(user: user)
    }
}

extension RegisterPresenter:InteractorToPresenterRegisterProtocol {
    func successfulyRegistered() {
        
    }
    
    func failureRegistered(errorText: String) {
        
    }
    
    
}
