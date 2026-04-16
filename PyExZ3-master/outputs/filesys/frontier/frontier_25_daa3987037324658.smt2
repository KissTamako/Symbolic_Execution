(set-logic ALL)
; Constraint ID: daa3987037324658
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60472)) (False)
(assert (not (= x 60472)))

; Query: ((== x 60473)) (False)
(assert (not (not (= x 60473))))

(check-sat)
(get-model)
