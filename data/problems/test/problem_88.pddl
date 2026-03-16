

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b10)
(on b2 b9)
(on b3 b8)
(ontable b4)
(on b5 b4)
(ontable b6)
(ontable b7)
(on b8 b1)
(on b9 b6)
(on b10 b5)
(clear b2)
(clear b3)
(clear b7)
)
(:goal
(and
(on b2 b9)
(on b4 b10)
(on b5 b1)
(on b6 b8)
(on b7 b4)
(on b8 b7)
(on b9 b3)
(on b10 b2))
)
)


