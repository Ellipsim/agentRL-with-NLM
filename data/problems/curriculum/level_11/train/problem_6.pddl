

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b11)
(on-table b2)
(on b3 b4)
(on-table b4)
(on b5 b9)
(on b6 b3)
(on b7 b1)
(on b8 b5)
(on b9 b2)
(on b10 b8)
(on-table b11)
(on-table b12)
(clear b6)
(clear b7)
(clear b10)
(clear b12)
)
(:goal
(and
(on b1 b11)
(on b2 b9)
(on b3 b6)
(on b4 b10)
(on b5 b12)
(on b7 b2)
(on b9 b8)
(on b10 b5))
)
)


