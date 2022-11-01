import Foundation

final class RegisterIneractor:PresenterToInteractorRegisterProtocol {
    
    var presenter: InteractorToPresenterRegisterProtocol?
    
    func registeringUser(user: RegisterUser) {
        let postURL = URL(string: Resources.Links.PostURL)!
        let registerRequest = RegisterRequest()
        registerRequest.postRequest(parameters: ["login":user.login,"mail":user.mail,"password":user.password], url: postURL) { statusCode, errorText in
            if let errorText = errorText {
                presenter?.failureRegistered(errorText: errorText)
                return
            }
            else if statusCode != nil {
                presenter?.successfulyRegistered()
            }
        }
    }
    
}
