(set-logic ALL)
; Constraint ID: 8a349da21d2cbca8
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60439)) (False)
(assert (not (= x 60439)))

; Query: ((== x 60440)) (False)
(assert (not (not (= x 60440))))

(check-sat)
(get-model)
