

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b9)
(on b2 b3)
(on-table b3)
(on b4 b11)
(on b5 b6)
(on b6 b8)
(on b7 b4)
(on b8 b7)
(on-table b9)
(on b10 b12)
(on b11 b1)
(on b12 b5)
(clear b2)
(clear b10)
)
(:goal
(and
(on b1 b9)
(on b2 b12)
(on b3 b7)
(on b4 b8)
(on b5 b2)
(on b6 b10)
(on b9 b3)
(on b10 b5)
(on b12 b1))
)
)


