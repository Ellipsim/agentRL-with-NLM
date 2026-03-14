

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b4)
(on b2 b11)
(on b3 b9)
(on b4 b7)
(on b5 b1)
(on-table b6)
(on b7 b8)
(on b8 b6)
(on b9 b10)
(on b10 b2)
(on-table b11)
(on b12 b3)
(clear b5)
(clear b12)
)
(:goal
(and
(on b1 b12)
(on b2 b10)
(on b3 b1)
(on b4 b6)
(on b5 b2)
(on b7 b4)
(on b8 b5)
(on b9 b8)
(on b11 b9)
(on b12 b7))
)
)


