

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(on b2 b8)
(on b3 b7)
(ontable b4)
(on b5 b9)
(on b6 b3)
(on b7 b1)
(on b8 b4)
(ontable b9)
(ontable b10)
(clear b2)
(clear b5)
(clear b6)
(clear b10)
)
(:goal
(and
(on b1 b8)
(on b2 b3)
(on b4 b9)
(on b6 b10)
(on b7 b4)
(on b8 b7)
(on b9 b6)
(on b10 b5))
)
)


