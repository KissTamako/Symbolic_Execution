(set-logic ALL)
; Constraint ID: 50876bc3dee7e095
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60295)) (False)
(assert (not (= x 60295)))

; Query: ((== x 60296)) (False)
(assert (not (not (= x 60296))))

(check-sat)
(get-model)
