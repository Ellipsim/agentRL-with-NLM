

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b6)
(ontable b3)
(on b4 b7)
(ontable b5)
(on b6 b5)
(on b7 b2)
(on b8 b10)
(ontable b9)
(ontable b10)
(clear b1)
(clear b4)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b5)
(on b3 b4)
(on b5 b10)
(on b7 b9)
(on b8 b7)
(on b10 b3))
)
)


