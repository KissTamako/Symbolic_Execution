(set-logic ALL)
; Constraint ID: ed4afca4c3f9b9e2
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59485)) (False)
(assert (not (= x 59485)))

; Query: ((== x 59486)) (False)
(assert (not (not (= x 59486))))

(check-sat)
(get-model)
