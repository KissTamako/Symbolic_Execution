(set-logic ALL)
; Constraint ID: afd5f03455f97650
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59941)) (False)
(assert (not (= x 59941)))

; Query: ((== x 59942)) (False)
(assert (not (not (= x 59942))))

(check-sat)
(get-model)
