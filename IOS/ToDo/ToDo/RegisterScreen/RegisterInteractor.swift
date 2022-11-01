import Foundation

final class RegisterIneractor:PresenterToInteractorRegisterProtocol {
    
    var presenter: InteractorToPresenterRegisterProtocol?
    
    func registeringUser(user: RegisterUser) {
        var test = RegisterRequest()
        test.postRequest()
    }
    
}
