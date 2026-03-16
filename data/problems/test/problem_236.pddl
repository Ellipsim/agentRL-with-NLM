

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(on b2 b11)
(on b3 b2)
(ontable b4)
(on b5 b3)
(on b6 b8)
(on b7 b6)
(on b8 b1)
(ontable b9)
(on b10 b12)
(ontable b11)
(on b12 b5)
(clear b4)
(clear b7)
(clear b9)
(clear b10)
)
(:goal
(and
(on b1 b4)
(on b3 b10)
(on b4 b5)
(on b5 b11)
(on b9 b12)
(on b11 b7))
)
)


