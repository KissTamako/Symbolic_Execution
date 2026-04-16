(set-logic ALL)
; Frontier Constraint ID: d63653b74d8c94d6
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1333)) (False)
(assert (not (= x 1333)))

; Query: ((== x 1334)) (False)
(assert (not (not (= x 1334))))

(check-sat)
(get-model)
