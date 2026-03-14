

(define (problem BW-rand-14)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 )
(:init
(arm-empty)
(on b1 b6)
(on b2 b10)
(on-table b3)
(on-table b4)
(on b5 b7)
(on b6 b12)
(on b7 b2)
(on b8 b3)
(on b9 b5)
(on b10 b13)
(on b11 b14)
(on b12 b4)
(on b13 b1)
(on b14 b8)
(clear b9)
(clear b11)
)
(:goal
(and
(on b1 b11)
(on b2 b7)
(on b5 b8)
(on b7 b4)
(on b8 b6)
(on b9 b1)
(on b12 b13)
(on b13 b3)
(on b14 b9))
)
)


