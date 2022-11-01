import UIKit

extension UIView {
    func addView(_ view:UIView) {
        view.translatesAutoresizingMaskIntoConstraints = false
        addSubview(view)
    }
}
