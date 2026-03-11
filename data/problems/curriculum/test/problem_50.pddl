

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b5)
(on-table b2)
(on b3 b2)
(on b4 b7)
(on-table b5)
(on b6 b3)
(on b7 b6)
(on b8 b10)
(on-table b9)
(on b10 b1)
(clear b4)
(clear b8)
(clear b9)
)
(:goal
(and
(on b2 b10)
(on b4 b5)
(on b5 b9)
(on b8 b6)
(on b9 b1)
(on b10 b7))
)
)


