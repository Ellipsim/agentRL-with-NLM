

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b3)
(on-table b2)
(on-table b3)
(on b4 b7)
(on-table b5)
(on-table b6)
(on b7 b2)
(on b8 b1)
(on b9 b5)
(on b10 b8)
(clear b4)
(clear b6)
(clear b9)
(clear b10)
)
(:goal
(and
(on b1 b3)
(on b4 b2)
(on b5 b10)
(on b6 b1)
(on b7 b6)
(on b8 b9)
(on b9 b4)
(on b10 b7))
)
)


