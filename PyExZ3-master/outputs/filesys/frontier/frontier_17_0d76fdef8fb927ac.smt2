(set-logic ALL)
; Constraint ID: 0d76fdef8fb927ac
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60460)) (False)
(assert (not (= x 60460)))

; Query: ((== x 60461)) (False)
(assert (not (not (= x 60461))))

(check-sat)
(get-model)
