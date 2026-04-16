(set-logic ALL)
; Constraint ID: b9c57c757dfa7e00
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60442)) (False)
(assert (not (not (= x 60442))))

(check-sat)
(get-model)
