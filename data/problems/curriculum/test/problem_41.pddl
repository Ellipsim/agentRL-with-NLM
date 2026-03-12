

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on-table b1)
(on-table b2)
(on b3 b10)
(on b4 b3)
(on b5 b12)
(on b6 b8)
(on b7 b1)
(on-table b8)
(on b9 b6)
(on b10 b11)
(on b11 b7)
(on b12 b9)
(on b13 b5)
(clear b2)
(clear b4)
(clear b13)
)
(:goal
(and
(on b2 b7)
(on b4 b6)
(on b6 b10)
(on b7 b3)
(on b8 b1)
(on b9 b11)
(on b13 b12))
)
)


